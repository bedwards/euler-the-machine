#!/usr/bin/env python3
"""Parse Gemini CLI session logs and extract key events, strategies, and metrics."""

import json
import sys
from datetime import datetime
from collections import defaultdict

def parse_timestamp(ts):
    """Parse ISO timestamp to datetime."""
    if ts:
        return datetime.fromisoformat(ts.replace('Z', '+00:00'))
    return None

def analyze_session(filepath):
    """Analyze a Gemini session log file."""
    with open(filepath) as f:
        data = json.load(f)

    messages = data.get('messages', [])
    session_start = parse_timestamp(data.get('startTime'))
    session_end = parse_timestamp(data.get('lastUpdated'))

    events = []
    thoughts = []
    tool_calls = defaultdict(int)
    searches = []
    final_answer = None
    answer_ts = None

    for msg in messages:
        ts = msg.get('timestamp')
        msg_type = msg.get('type')
        content = msg.get('content', '')

        # Track thoughts (Gemini's internal reasoning)
        if 'thoughts' in msg:
            for thought in msg['thoughts']:
                thoughts.append({
                    'timestamp': thought.get('timestamp'),
                    'subject': thought.get('subject', ''),
                    'description': thought.get('description', '')[:300]
                })

        # Track tool calls
        if 'toolCalls' in msg:
            for tc in msg['toolCalls']:
                tool_name = tc.get('toolName', 'unknown')
                tool_calls[tool_name] += 1

                # Track web searches specifically
                args = tc.get('args', {})
                if 'Search' in tool_name or 'search' in str(args):
                    query = args.get('query', '') if isinstance(args, dict) else str(args)
                    searches.append({
                        'timestamp': ts,
                        'query': query[:100] if query else ''
                    })

        # Track OEIS/Project Euler references
        if 'OEIS' in content or 'Project Euler' in content:
            events.append({
                'timestamp': ts,
                'type': 'research_reference',
                'content': content[:300]
            })

        # Look for final answer
        if 'best guess' in content.lower():
            events.append({
                'timestamp': ts,
                'type': 'final_answer',
                'content': content[:500]
            })
            # Extract the number
            if '780166455' in content:
                final_answer = '780166455'
                answer_ts = parse_timestamp(ts)

    # Calculate duration
    total_duration = None
    if session_start and session_end:
        total_duration = session_end - session_start

    return {
        'session_id': data.get('sessionId'),
        'total_messages': len(messages),
        'first_timestamp': session_start.isoformat() if session_start else None,
        'last_timestamp': session_end.isoformat() if session_end else None,
        'total_duration': str(total_duration) if total_duration else None,
        'tool_calls': dict(tool_calls),
        'thoughts': thoughts,
        'searches': searches,
        'events': events,
        'final_answer': final_answer,
        'found_correct_answer': final_answer == '798443574'
    }

def main():
    if len(sys.argv) < 2:
        filepath = '/Users/bedwards/.gemini/tmp/9d2085b3dda8afe1a6ba949f5cac9c4f79471760d71742e22791b0b95595aca1/chats/session-2026-01-22T01-17-847d597b.json'
    else:
        filepath = sys.argv[1]

    print(f"Analyzing Gemini session log: {filepath}\n")
    results = analyze_session(filepath)

    print("=" * 60)
    print("GEMINI SESSION ANALYSIS")
    print("=" * 60)
    print(f"Session ID: {results['session_id']}")
    print(f"Total messages: {results['total_messages']}")
    print(f"Session start: {results['first_timestamp']}")
    print(f"Session end: {results['last_timestamp']}")
    print(f"Total duration: {results['total_duration']}")
    print(f"Final answer given: {results['final_answer']}")
    print(f"Found correct answer: {results['found_correct_answer']}")

    print("\n--- Tool Usage ---")
    for tool, count in sorted(results['tool_calls'].items(), key=lambda x: -x[1]):
        print(f"  {tool}: {count}")

    print("\n--- Thoughts (sample) ---")
    for thought in results['thoughts'][:10]:
        print(f"\n  [{thought['timestamp']}] {thought['subject']}")
        print(f"  {thought['description'][:150]}...")

    # Output as JSON
    with open('/Users/bedwards/euler-the-machine/tools/gemini_analysis.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n\nFull analysis saved to gemini_analysis.json")

if __name__ == '__main__':
    main()
