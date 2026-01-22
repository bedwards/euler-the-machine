#!/usr/bin/env python3
"""Generate summary markdown files for each AI system's session."""

import json
from datetime import datetime
from pathlib import Path

# Session log paths
CLAUDE_LOG = '/Users/bedwards/.claude/projects/-Users-bedwards-euler-the-machine-contestants-claude/fe66f3cb-cd97-4abf-b267-a6bbda8671a3.jsonl'
CODEX_LOG = '/Users/bedwards/.codex/sessions/2026/01/21/rollout-2026-01-21T19-20-06-019be349-8bef-7dd1-96de-301c06e66e25.jsonl'
GEMINI_LOG = '/Users/bedwards/.gemini/tmp/9d2085b3dda8afe1a6ba949f5cac9c4f79471760d71742e22791b0b95595aca1/chats/session-2026-01-22T01-17-847d597b.json'

OUTPUT_DIR = Path('/Users/bedwards/euler-the-machine/summaries')

def parse_timestamp(ts):
    if ts:
        return datetime.fromisoformat(ts.replace('Z', '+00:00'))
    return None

def analyze_claude():
    """Deep analysis of Claude session."""
    with open(CLAUDE_LOG) as f:
        lines = f.readlines()

    events = []
    first_ts = None
    last_ts = None
    answer_ts = None
    project_euler_ts = None

    for i, line in enumerate(lines):
        try:
            data = json.loads(line)
            ts = data.get('timestamp')

            if ts:
                parsed_ts = parse_timestamp(ts)
                if first_ts is None:
                    first_ts = parsed_ts
                last_ts = parsed_ts

            # Check for answer
            if '798443574' in line and answer_ts is None:
                answer_ts = parse_timestamp(ts)
                events.append(f"**{ts}**: ✅ CORRECT ANSWER FOUND: 798443574")

            # Check for Project Euler recognition
            if 'Project Euler' in line and project_euler_ts is None:
                project_euler_ts = parse_timestamp(ts)
                events.append(f"**{ts}**: 🔍 Recognized as Project Euler problem")

            # Check for OEIS searches
            if 'OEIS' in line:
                events.append(f"**{ts}**: 📖 Referenced OEIS")

            # Extract key strategy moments from assistant messages
            if data.get('type') == 'assistant':
                msg = data.get('message', {})
                content = msg.get('content', '')
                if isinstance(content, list):
                    for item in content:
                        if isinstance(item, dict) and 'text' in item:
                            text = item['text']
                            if any(kw in text.lower() for kw in ['recurrence', 'formula', 'dynamic programming', 'brute force', 'approach']):
                                if len(text) > 100:
                                    events.append(f"**{ts}**: Strategy: {text[:150]}...")

        except json.JSONDecodeError:
            continue

    duration = last_ts - first_ts if first_ts and last_ts else None
    time_to_answer = answer_ts - first_ts if first_ts and answer_ts else None

    return {
        'name': 'Claude (Opus 4.5)',
        'version': '2.1.15 (Claude Code)',
        'model': 'claude-opus-4-5-20251101',
        'start_time': first_ts,
        'end_time': last_ts,
        'duration': duration,
        'answer_time': answer_ts,
        'time_to_answer': time_to_answer,
        'project_euler_recognized': project_euler_ts,
        'final_answer': '798443574',
        'correct': True,
        'events': events[:30],  # Limit events
        'total_lines': len(lines)
    }

def analyze_codex():
    """Deep analysis of Codex session."""
    with open(CODEX_LOG) as f:
        lines = f.readlines()

    events = []
    reasoning = []
    first_ts = None
    last_ts = None
    project_euler_ts = None

    for i, line in enumerate(lines):
        try:
            data = json.loads(line)
            ts = data.get('timestamp')
            payload = data.get('payload', {})

            if ts:
                parsed_ts = parse_timestamp(ts)
                if first_ts is None:
                    first_ts = parsed_ts
                last_ts = parsed_ts

            # Check for Project Euler recognition
            if 'Project Euler' in line and project_euler_ts is None:
                project_euler_ts = parse_timestamp(ts)

            # Extract reasoning events
            if data.get('type') == 'event_msg' and payload.get('type') == 'agent_reasoning':
                text = payload.get('text', '')
                reasoning.append({
                    'timestamp': ts,
                    'text': text
                })
                if len(text) > 50:
                    events.append(f"**{ts}**: {text[:200]}...")

        except json.JSONDecodeError:
            continue

    duration = last_ts - first_ts if first_ts and last_ts else None

    return {
        'name': 'Codex (GPT-5.2)',
        'version': '0.88.0 (codex-cli)',
        'model': 'gpt-5.2-codex high',
        'start_time': first_ts,
        'end_time': last_ts,
        'duration': duration,
        'answer_time': None,
        'time_to_answer': None,
        'project_euler_recognized': project_euler_ts,
        'final_answer': '884983106',
        'correct': False,
        'events': events[:30],
        'reasoning': reasoning,
        'total_lines': len(lines)
    }

def analyze_gemini():
    """Deep analysis of Gemini session."""
    with open(GEMINI_LOG) as f:
        data = json.load(f)

    messages = data.get('messages', [])
    first_ts = parse_timestamp(data.get('startTime'))
    last_ts = parse_timestamp(data.get('lastUpdated'))

    events = []
    thoughts = []
    project_euler_ts = None
    oeis_ts = None

    for msg in messages:
        ts = msg.get('timestamp')
        content = msg.get('content', '')

        # Check for Project Euler recognition
        if 'Project Euler' in str(msg) and project_euler_ts is None:
            project_euler_ts = parse_timestamp(ts)
            events.append(f"**{ts}**: 🔍 Searched for Project Euler 763")

        # Check for OEIS searches
        if 'OEIS' in str(msg) and oeis_ts is None:
            oeis_ts = parse_timestamp(ts)
            events.append(f"**{ts}**: 📖 Searched OEIS for sequence")

        # Extract thoughts
        if 'thoughts' in msg:
            for thought in msg['thoughts']:
                thoughts.append({
                    'timestamp': thought.get('timestamp'),
                    'subject': thought.get('subject', ''),
                    'description': thought.get('description', '')
                })
                events.append(f"**{thought.get('timestamp')}**: 💭 {thought.get('subject')}: {thought.get('description', '')[:100]}...")

    duration = last_ts - first_ts if first_ts and last_ts else None

    return {
        'name': 'Gemini (3-Pro Preview)',
        'version': '0.25.0 (gemini-cli)',
        'model': 'gemini-3-pro-preview',
        'start_time': first_ts,
        'end_time': last_ts,
        'duration': duration,
        'answer_time': None,
        'time_to_answer': None,
        'project_euler_recognized': project_euler_ts,
        'oeis_searched': oeis_ts,
        'final_answer': '780166455',
        'correct': False,
        'events': events[:40],
        'thoughts': thoughts,
        'total_messages': len(messages)
    }

def generate_markdown(analysis, filename):
    """Generate markdown summary for a system."""
    md = f"""# {analysis['name']} Session Summary

## Overview

| Metric | Value |
|--------|-------|
| Version | {analysis['version']} |
| Model | {analysis['model']} |
| Start Time | {analysis['start_time']} |
| End Time | {analysis['end_time']} |
| Total Duration | {analysis['duration']} |
| Time to Answer | {analysis.get('time_to_answer', 'N/A')} |
| Final Answer | {analysis['final_answer']} |
| Correct | {'✅ Yes' if analysis['correct'] else '❌ No'} |

## Key Recognition Moments

- Recognized as Project Euler: {analysis.get('project_euler_recognized', 'Never')}
- OEIS Referenced: {analysis.get('oeis_searched', 'N/A')}

## Timeline of Key Events

"""

    for event in analysis.get('events', []):
        md += f"- {event}\n"

    OUTPUT_DIR.mkdir(exist_ok=True)
    with open(OUTPUT_DIR / filename, 'w') as f:
        f.write(md)

    print(f"Generated: {OUTPUT_DIR / filename}")

def main():
    print("Analyzing Claude session...")
    claude = analyze_claude()
    generate_markdown(claude, 'claude_summary.md')

    print("\nAnalyzing Codex session...")
    codex = analyze_codex()
    generate_markdown(codex, 'codex_summary.md')

    print("\nAnalyzing Gemini session...")
    gemini = analyze_gemini()
    generate_markdown(gemini, 'gemini_summary.md')

    # Generate comparison markdown
    comparison = f"""# AI Coding Agent Comparison: Project Euler 763

## The Challenge

Project Euler Problem 763 "Amoebas in a 3D Grid" asks for D(10000) mod 10^9, where D(N) counts distinct amoeba arrangements after N divisions.

**Correct Answer: 798443574**

## Results Summary

| System | Duration | Final Answer | Correct | Recognized PE |
|--------|----------|--------------|---------|---------------|
| Claude (Opus 4.5) | {claude['duration']} | {claude['final_answer']} | ✅ | {'Yes' if claude['project_euler_recognized'] else 'No'} |
| Codex (GPT-5.2) | {codex['duration']} | {codex['final_answer']} | ❌ | {'Yes' if codex['project_euler_recognized'] else 'No'} |
| Gemini (3-Pro) | {gemini['duration']} | {gemini['final_answer']} | ❌ | {'Yes' if gemini['project_euler_recognized'] else 'No'} |

## Key Observations

### Claude (Winner)
- Found the correct answer in {claude.get('time_to_answer', 'N/A')}
- Successfully identified this as Project Euler 763
- Used a combination of mathematical insight and verification

### Codex
- Ran for {codex['duration']}
- Did not search for external resources (OEIS, Project Euler)
- Final guess: {codex['final_answer']} (incorrect)

### Gemini
- Ran for {gemini['duration']}
- Searched OEIS and Project Euler
- Gave up and returned D(100) as "best guess": {gemini['final_answer']} (incorrect)
"""

    with open(OUTPUT_DIR / 'comparison.md', 'w') as f:
        f.write(comparison)
    print(f"\nGenerated: {OUTPUT_DIR / 'comparison.md'}")

if __name__ == '__main__':
    main()
