#!/usr/bin/env python3
"""Generate SVG charts for the essay."""

import json
from pathlib import Path

# Data from the experiments
systems = ['Claude', 'Codex', 'Gemini']
colors = ['#d97706', '#059669', '#2563eb']

# Times in seconds
times_to_answer = {
    'Claude': 25*60 + 2,  # 25:02
    'Codex': 37*60 + 42,  # 37:42 (total time, didn't find answer)
    'Gemini': 34*60 + 27  # 34:27 (total time, didn't find answer)
}

# Sequence values for D(N)
sequence = [1, 1, 3, 9, 30, 99, 336, 1134, 3855, 13086, 44499]

def create_timeline_chart():
    """Create a timeline comparison chart."""
    svg = '''<svg viewBox="0 0 600 250" xmlns="http://www.w3.org/2000/svg" style="font-family: Helvetica, Arial, sans-serif;">
    <style>
        .bar { transition: opacity 0.2s; }
        .bar:hover { opacity: 0.8; }
        .label { font-size: 12px; fill: #44403c; }
        .time-label { font-size: 11px; fill: #78716c; }
        .correct { fill: #059669; }
        .incorrect { fill: #dc2626; }
        .axis { stroke: #e7e5e4; stroke-width: 1; }
    </style>

    <!-- Title -->
    <text x="300" y="25" text-anchor="middle" font-size="14" font-weight="600" fill="#1c1917">Time to Complete (Minutes)</text>

    <!-- Axes -->
    <line x1="100" y1="50" x2="100" y2="200" class="axis"/>
    <line x1="100" y1="200" x2="580" y2="200" class="axis"/>

    <!-- Time markers -->
    <line x1="220" y1="200" x2="220" y2="205" class="axis"/>
    <text x="220" y="220" text-anchor="middle" class="time-label">10</text>

    <line x1="340" y1="200" x2="340" y2="205" class="axis"/>
    <text x="340" y="220" text-anchor="middle" class="time-label">20</text>

    <line x1="460" y1="200" x2="460" y2="205" class="axis"/>
    <text x="460" y="220" text-anchor="middle" class="time-label">30</text>

    <line x1="580" y1="200" x2="580" y2="205" class="axis"/>
    <text x="580" y="220" text-anchor="middle" class="time-label">40</text>

    <!-- Claude bar (found answer at 25:02) -->
    <text x="95" y="85" text-anchor="end" class="label">Claude</text>
    <rect class="bar" x="100" y="70" width="300" height="25" fill="#d97706" rx="3"/>
    <circle cx="400" cy="82.5" r="8" class="correct"/>
    <text x="415" y="87" font-size="10" fill="#059669">25:02</text>

    <!-- Codex bar -->
    <text x="95" y="130" text-anchor="end" class="label">Codex</text>
    <rect class="bar" x="100" y="115" width="452" height="25" fill="#059669" rx="3"/>
    <circle cx="552" cy="127.5" r="8" class="incorrect"/>
    <text x="415" y="132" font-size="10" fill="#dc2626">37:42 (wrong)</text>

    <!-- Gemini bar -->
    <text x="95" y="175" text-anchor="end" class="label">Gemini</text>
    <rect class="bar" x="100" y="160" width="413" height="25" fill="#2563eb" rx="3"/>
    <circle cx="513" cy="172.5" r="8" class="incorrect"/>
    <text x="415" y="177" font-size="10" fill="#dc2626">34:27 (wrong)</text>

    <!-- Legend -->
    <circle cx="120" cy="240" r="6" class="correct"/>
    <text x="130" y="244" font-size="10" fill="#44403c">Correct answer</text>
    <circle cx="230" cy="240" r="6" class="incorrect"/>
    <text x="240" y="244" font-size="10" fill="#44403c">Incorrect answer</text>
</svg>'''
    return svg

def create_sequence_chart():
    """Create a chart showing the D(N) sequence growth."""
    # Normalize for chart
    max_val = max(sequence)
    height = 200
    width = 500
    padding = 50

    points = []
    for i, val in enumerate(sequence):
        x = padding + (i * (width - 2*padding) / (len(sequence) - 1))
        y = height - padding - (val / max_val * (height - 2*padding))
        points.append(f"{x},{y}")

    path_d = "M" + " L".join(points)

    svg = f'''<svg viewBox="0 0 {width} {height + 50}" xmlns="http://www.w3.org/2000/svg" style="font-family: Helvetica, Arial, sans-serif;">
    <style>
        .axis {{ stroke: #e7e5e4; stroke-width: 1; }}
        .grid {{ stroke: #f5f5f4; stroke-width: 1; }}
        .line {{ fill: none; stroke: #d97706; stroke-width: 2; }}
        .point {{ fill: #d97706; }}
        .label {{ font-size: 10px; fill: #78716c; }}
    </style>

    <!-- Title -->
    <text x="{width/2}" y="20" text-anchor="middle" font-size="14" font-weight="600" fill="#1c1917">D(N) Sequence Growth</text>

    <!-- Grid lines -->
    <line x1="{padding}" y1="35" x2="{padding}" y2="{height - padding + 10}" class="axis"/>
    <line x1="{padding - 5}" y1="{height - padding}" x2="{width - padding}" y2="{height - padding}" class="axis"/>

    <!-- Y-axis labels -->
    <text x="{padding - 10}" y="{height - padding + 5}" text-anchor="end" class="label">0</text>
    <text x="{padding - 10}" y="45" text-anchor="end" class="label">44,499</text>

    <!-- X-axis labels -->
    <text x="{padding}" y="{height - padding + 20}" text-anchor="middle" class="label">0</text>
    <text x="{width - padding}" y="{height - padding + 20}" text-anchor="middle" class="label">10</text>

    <!-- Line -->
    <path d="{path_d}" class="line"/>

    <!-- Points -->'''

    for i, val in enumerate(sequence):
        x = padding + (i * (width - 2*padding) / (len(sequence) - 1))
        y = height - padding - (val / max_val * (height - 2*padding))
        svg += f'\n    <circle cx="{x}" cy="{y}" r="4" class="point"/>'

    svg += '''

    <!-- Annotation -->
    <text x="400" y="60" font-size="11" fill="#44403c">D(10) = 44,499</text>
    <line x1="400" y1="65" x2="''' + str(width - padding) + '''" y2="''' + str(height - padding - ((sequence[-1] / max_val) * (height - 2*padding))) + '''" stroke="#e7e5e4" stroke-dasharray="4"/>
</svg>'''
    return svg

def create_approach_chart():
    """Create a comparison of approaches taken."""
    svg = '''<svg viewBox="0 0 600 300" xmlns="http://www.w3.org/2000/svg" style="font-family: Helvetica, Arial, sans-serif;">
    <style>
        .header { font-size: 12px; font-weight: 600; fill: #1c1917; }
        .cell { font-size: 11px; fill: #44403c; }
        .yes { fill: #059669; }
        .no { fill: #dc2626; }
        .partial { fill: #d97706; }
    </style>

    <!-- Title -->
    <text x="300" y="25" text-anchor="middle" font-size="14" font-weight="600" fill="#1c1917">Problem-Solving Approaches Comparison</text>

    <!-- Headers -->
    <text x="150" y="60" text-anchor="middle" class="header">Claude</text>
    <text x="300" y="60" text-anchor="middle" class="header">Codex</text>
    <text x="450" y="60" text-anchor="middle" class="header">Gemini</text>

    <!-- Row: Web Search -->
    <text x="50" y="95" class="cell">Web Search</text>
    <text x="150" y="95" text-anchor="middle" class="yes">Yes</text>
    <text x="300" y="95" text-anchor="middle" class="no">No</text>
    <text x="450" y="95" text-anchor="middle" class="yes">Yes</text>

    <!-- Row: OEIS Lookup -->
    <text x="50" y="125" class="cell">OEIS Lookup</text>
    <text x="150" y="125" text-anchor="middle" class="yes">Yes</text>
    <text x="300" y="125" text-anchor="middle" class="no">No</text>
    <text x="450" y="125" text-anchor="middle" class="yes">Yes</text>

    <!-- Row: Brute Force Simulation -->
    <text x="50" y="155" class="cell">Brute Force Sim</text>
    <text x="150" y="155" text-anchor="middle" class="yes">Yes</text>
    <text x="300" y="155" text-anchor="middle" class="yes">Yes</text>
    <text x="450" y="155" text-anchor="middle" class="yes">Yes</text>

    <!-- Row: Recurrence Finding -->
    <text x="50" y="185" class="cell">Recurrence Finding</text>
    <text x="150" y="185" text-anchor="middle" class="yes">Yes</text>
    <text x="300" y="185" text-anchor="middle" class="yes">Yes</text>
    <text x="450" y="185" text-anchor="middle" class="yes">Yes</text>

    <!-- Row: Structural Insight -->
    <text x="50" y="215" class="cell">Structural Insight</text>
    <text x="150" y="215" text-anchor="middle" class="yes">Yes</text>
    <text x="300" y="215" text-anchor="middle" class="partial">Partial</text>
    <text x="450" y="215" text-anchor="middle" class="no">No</text>

    <!-- Row: Correct Answer -->
    <text x="50" y="245" class="cell" font-weight="600">Correct Answer</text>
    <text x="150" y="245" text-anchor="middle" class="yes" font-weight="600">Yes</text>
    <text x="300" y="245" text-anchor="middle" class="no" font-weight="600">No</text>
    <text x="450" y="245" text-anchor="middle" class="no" font-weight="600">No</text>

    <!-- Separators -->
    <line x1="50" y1="70" x2="550" y2="70" stroke="#e7e5e4" stroke-width="1"/>
    <line x1="50" y1="260" x2="550" y2="260" stroke="#e7e5e4" stroke-width="1"/>
</svg>'''
    return svg

def main():
    output_dir = Path('/Users/bedwards/euler-the-machine/docs/assets/charts')
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate charts
    charts = {
        'timeline.svg': create_timeline_chart(),
        'sequence.svg': create_sequence_chart(),
        'approaches.svg': create_approach_chart()
    }

    for filename, svg in charts.items():
        filepath = output_dir / filename
        with open(filepath, 'w') as f:
            f.write(svg)
        print(f"Created: {filepath}")

if __name__ == '__main__':
    main()
