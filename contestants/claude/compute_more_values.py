#!/usr/bin/env python3
"""
Compute more values of D(n) using optimized enumeration.
"""

from functools import lru_cache
import sys

def get_next_states(current_config):
    """Generate all states reachable by one division."""
    next_states = set()
    for (x, y, z) in current_config:
        c1 = (x + 1, y, z)
        c2 = (x, y + 1, z)
        c3 = (x, y, z + 1)
        if c1 not in current_config and c2 not in current_config and c3 not in current_config:
            new_config = set(current_config)
            new_config.remove((x, y, z))
            new_config.add(c1)
            new_config.add(c2)
            new_config.add(c3)
            next_states.add(frozenset(new_config))
    return next_states

def solve_brute_force(max_n):
    """Brute force enumeration."""
    current_layer = {frozenset([(0, 0, 0)])}
    values = [1]

    for n in range(1, max_n + 1):
        next_layer = set()
        for config in current_layer:
            next_layer.update(get_next_states(config))
        current_layer = next_layer
        values.append(len(current_layer))
        print(f"D({n}) = {len(current_layer)}")
        sys.stdout.flush()

    return values

if __name__ == "__main__":
    max_n = 15
    if len(sys.argv) > 1:
        max_n = int(sys.argv[1])

    print(f"Computing D(n) for n = 0 to {max_n}")
    values = solve_brute_force(max_n)

    print("\nFinal values:")
    print("D =", values)
