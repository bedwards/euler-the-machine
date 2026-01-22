#!/usr/bin/env python3
"""Parse Codex CLI session logs and extract key events, strategies, and metrics."""

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
    """Analyze a Codex session log file."""
    with open(filepath) as f:
        lines = f.readlines()

    events = []
    tool_calls = defaultdict(int)
    reasoning_events = []
    first_ts = None
    last_ts = None
    answer_ts = None
    final_answer = None

    for i, line in enumerate(lines):
        try:
            data = json.loads(line)
            ts = data.get('timestamp')
            event_type = data.get('type')
            payload = data.get('payload', {})

            if ts:
                parsed_ts = parse_timestamp(ts)
                if first_ts is None:
                    first_ts = parsed_ts
                last_ts = parsed_ts

            # Track reasoning events (Codex uses agent_reasoning)
            if event_type == 'event_msg':
                msg_type = payload.get('type')
                if msg_type == 'agent_reasoning':
                    text = payload.get('text', '')
                    reasoning_events.append({
                        'line': i + 1,
                        'timestamp': ts,
                        'text': text[:500] if len(text) > 500 else text
                    })

            # Track tool use
            if event_type == 'response_item':
                item_type = payload.get('type')
                if item_type == 'function_call':
                    func_name = payload.get('name', 'unknown')
                    tool_calls[func_name] += 1

            # Track user interrupts and final answer requests
            if 'Time to quit' in line or 'What is the answer' in line:
                events.append({
                    'line': i + 1,
                    'timestamp': ts,
                    'type': 'user_interrupt',
                    'content': line[:200]
                })

            # Look for final answer
            if '884983106' in line:
                if answer_ts is None:
                    answer_ts = parse_timestamp(ts)
                    final_answer = '884983106'

        except json.JSONDecodeError:
            continue

    # Calculate durations
    total_duration = None
    if first_ts and last_ts:
        total_duration = last_ts - first_ts

    return {
        'total_lines': len(lines),
        'first_timestamp': first_ts.isoformat() if first_ts else None,
        'last_timestamp': last_ts.isoformat() if last_ts else None,
        'total_duration': str(total_duration) if total_duration else None,
        'tool_calls': dict(tool_calls),
        'reasoning_events': reasoning_events,
        'final_answer': final_answer,
        'found_correct_answer': final_answer == '798443574',
        'events': events
    }

def main():
    if len(sys.argv) < 2:
        filepath = '/Users/bedwards/.codex/sessions/2026/01/21/rollout-2026-01-21T19-20-06-019be349-8bef-7dd1-96de-301c06e66e25.jsonl'
    else:
        filepath = sys.argv[1]

    print(f"Analyzing Codex session log: {filepath}\n")
    results = analyze_session(filepath)

    print("=" * 60)
    print("CODEX SESSION ANALYSIS")
    print("=" * 60)
    print(f"Total log lines: {results['total_lines']}")
    print(f"Session start: {results['first_timestamp']}")
    print(f"Session end: {results['last_timestamp']}")
    print(f"Total duration: {results['total_duration']}")
    print(f"Final answer given: {results['final_answer']}")
    print(f"Found correct answer: {results['found_correct_answer']}")

    print("\n--- Tool Usage ---")
    for tool, count in sorted(results['tool_calls'].items(), key=lambda x: -x[1]):
        print(f"  {tool}: {count}")

    print("\n--- Reasoning Events (sample) ---")
    for event in results['reasoning_events'][:10]:
        print(f"\n  [{event['timestamp']}]")
        print(f"  {event['text'][:200]}...")

    # Output as JSON
    with open('/Users/bedwards/euler-the-machine/tools/codex_analysis.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n\nFull analysis saved to codex_analysis.json")

if __name__ == '__main__':
    main()
