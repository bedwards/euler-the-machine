# AI Coding Agent Comparison: Project Euler 763

## The Challenge

Project Euler Problem 763 "Amoebas in a 3D Grid" asks for D(10000) mod 10^9, where D(N) counts distinct amoeba arrangements after N divisions.

**Correct Answer: 798443574**

## Results Summary

| System | Duration | Final Answer | Correct | Recognized PE |
|--------|----------|--------------|---------|---------------|
| Claude (Opus 4.5) | 0:30:35.465000 | 798443574 | ✅ | Yes |
| Codex (GPT-5.2) | 0:37:41.894000 | 884983106 | ❌ | No |
| Gemini (3-Pro) | 0:34:27.022000 | 780166455 | ❌ | Yes |

## Key Observations

### Claude (Winner)
- Found the correct answer in 0:25:02.182000
- Successfully identified this as Project Euler 763
- Used a combination of mathematical insight and verification

### Codex
- Ran for 0:37:41.894000
- Did not search for external resources (OEIS, Project Euler)
- Final guess: 884983106 (incorrect)

### Gemini
- Ran for 0:34:27.022000
- Searched OEIS and Project Euler
- Gave up and returned D(100) as "best guess": 780166455 (incorrect)
