#!/usr/bin/env python3
"""Parse Claude Code session logs and extract key events, strategies, and metrics."""

import json
import sys
from datetime import datetime
from collections import defaultdict
import re

def parse_timestamp(ts):
    """Parse ISO timestamp to datetime."""
    if ts:
        return datetime.fromisoformat(ts.replace('Z', '+00:00'))
    return None

def extract_text_content(content):
    """Extract text from various content formats."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        texts = []
        for item in content:
            if isinstance(item, dict):
                if 'text' in item:
                    texts.append(item['text'])
                elif 'content' in item:
                    texts.append(extract_text_content(item['content']))
            elif isinstance(item, str):
                texts.append(item)
        return '\n'.join(texts)
    if isinstance(content, dict):
        if 'text' in content:
            return content['text']
        if 'content' in content:
            return extract_text_content(content['content'])
    return str(content)

def analyze_session(filepath):
    """Analyze a Claude session log file."""
    with open(filepath) as f:
        lines = f.readlines()

    events = []
    tool_calls = defaultdict(int)
    strategies = []
    key_findings = []
    errors = []
    first_ts = None
    last_ts = None
    answer_ts = None
    total_input_tokens = 0
    total_output_tokens = 0

    # Keywords indicating strategy changes or important moments
    strategy_keywords = [
        'approach', 'strategy', 'try', 'attempt', 'explore', 'investigate',
        'recurrence', 'formula', 'pattern', 'OEIS', 'Project Euler',
        'dynamic programming', 'brute force', 'simulation', 'generate',
        'compute', 'verify', 'check', 'result', 'answer', 'solution'
    ]

    for i, line in enumerate(lines):
        try:
            data = json.loads(line)
            ts = data.get('timestamp')

            if ts:
                parsed_ts = parse_timestamp(ts)
                if first_ts is None:
                    first_ts = parsed_ts
                last_ts = parsed_ts

            event_type = data.get('type')

            # Track answer discovery
            if '798443574' in line and answer_ts is None:
                answer_ts = parse_timestamp(ts)
                key_findings.append({
                    'line': i + 1,
                    'timestamp': ts,
                    'event': 'CORRECT ANSWER FOUND: 798443574'
                })

            # Track tool calls
            if event_type == 'tool_use':
                tool_name = data.get('name', 'unknown')
                tool_calls[tool_name] += 1

            # Track assistant messages for strategy analysis
            if event_type == 'assistant':
                content = extract_text_content(data.get('message', {}).get('content', ''))

                # Look for strategy keywords
                content_lower = content.lower()
                for kw in strategy_keywords:
                    if kw.lower() in content_lower:
                        # Check if this is a significant statement
                        if len(content) > 50:  # Ignore very short messages
                            events.append({
                                'line': i + 1,
                                'timestamp': ts,
                                'type': 'strategy',
                                'keyword': kw,
                                'excerpt': content[:200] + '...' if len(content) > 200 else content
                            })
                            break

            # Track errors
            if 'error' in line.lower():
                events.append({
                    'line': i + 1,
                    'timestamp': ts,
                    'type': 'error',
                    'content': line[:300]
                })

            # Track token usage
            if 'usage' in data:
                usage = data.get('usage', {})
                total_input_tokens += usage.get('input_tokens', 0)
                total_output_tokens += usage.get('output_tokens', 0)

        except json.JSONDecodeError:
            continue

    # Calculate durations
    total_duration = None
    time_to_answer = None
    if first_ts and last_ts:
        total_duration = last_ts - first_ts
    if first_ts and answer_ts:
        time_to_answer = answer_ts - first_ts

    return {
        'total_lines': len(lines),
        'first_timestamp': first_ts.isoformat() if first_ts else None,
        'last_timestamp': last_ts.isoformat() if last_ts else None,
        'answer_timestamp': answer_ts.isoformat() if answer_ts else None,
        'total_duration': str(total_duration) if total_duration else None,
        'time_to_answer': str(time_to_answer) if time_to_answer else None,
        'tool_calls': dict(tool_calls),
        'total_input_tokens': total_input_tokens,
        'total_output_tokens': total_output_tokens,
        'key_findings': key_findings,
        'strategy_events': events[:50],  # Limit to first 50 events
        'found_correct_answer': answer_ts is not None
    }

def main():
    if len(sys.argv) < 2:
        filepath = '/Users/bedwards/.claude/projects/-Users-bedwards-euler-the-machine-contestants-claude/fe66f3cb-cd97-4abf-b267-a6bbda8671a3.jsonl'
    else:
        filepath = sys.argv[1]

    print(f"Analyzing Claude session log: {filepath}\n")
    results = analyze_session(filepath)

    print("=" * 60)
    print("CLAUDE SESSION ANALYSIS")
    print("=" * 60)
    print(f"Total log lines: {results['total_lines']}")
    print(f"Session start: {results['first_timestamp']}")
    print(f"Session end: {results['last_timestamp']}")
    print(f"Total duration: {results['total_duration']}")
    print(f"Time to answer: {results['time_to_answer']}")
    print(f"Found correct answer: {results['found_correct_answer']}")
    print(f"Total input tokens: {results['total_input_tokens']}")
    print(f"Total output tokens: {results['total_output_tokens']}")

    print("\n--- Tool Usage ---")
    for tool, count in sorted(results['tool_calls'].items(), key=lambda x: -x[1]):
        print(f"  {tool}: {count}")

    print("\n--- Key Findings ---")
    for finding in results['key_findings']:
        print(f"  Line {finding['line']} ({finding['timestamp']}): {finding['event']}")

    # Output as JSON for further processing
    with open('/Users/bedwards/euler-the-machine/tools/claude_analysis.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nFull analysis saved to claude_analysis.json")

if __name__ == '__main__':
    main()
