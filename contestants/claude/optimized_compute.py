#!/usr/bin/env python3
"""
Optimized computation of D(n) using canonical representation of configurations.
"""

import sys
from collections import defaultdict

def canonical_form(config):
    """
    Return a canonical (rotation/reflection-invariant) form of a configuration.
    For now, just use the configuration as-is but sorted.
    """
    return frozenset(config)

def get_next_states_fast(current_config):
    """Generate all states reachable by one division, using a set for fast lookup."""
    config_set = set(current_config)
    next_states = set()

    for (x, y, z) in current_config:
        c1 = (x + 1, y, z)
        c2 = (x, y + 1, z)
        c3 = (x, y, z + 1)

        if c1 not in config_set and c2 not in config_set and c3 not in config_set:
            new_config = config_set.copy()
            new_config.remove((x, y, z))
            new_config.add(c1)
            new_config.add(c2)
            new_config.add(c3)
            next_states.add(frozenset(new_config))

    return next_states

def solve_iterative(max_n):
    """Iteratively compute D(n)."""
    current_layer = {frozenset([(0, 0, 0)])}
    values = [1]  # D(0) = 1

    for n in range(1, max_n + 1):
        next_layer = set()
        for config in current_layer:
            next_layer.update(get_next_states_fast(config))
        current_layer = next_layer
        values.append(len(current_layer))
        print(f"D({n}) = {len(current_layer)}, configurations in memory: {len(current_layer)}")
        sys.stdout.flush()

    return values

# Use multiprocessing to speed up
from multiprocessing import Pool, cpu_count

def process_config(config):
    """Process a single configuration."""
    return get_next_states_fast(config)

def solve_parallel(max_n, num_workers=None):
    """Parallel computation of D(n)."""
    if num_workers is None:
        num_workers = cpu_count()

    current_layer = {frozenset([(0, 0, 0)])}
    values = [1]

    for n in range(1, max_n + 1):
        next_layer = set()

        # For small layers, don't bother with parallelism
        if len(current_layer) < 1000:
            for config in current_layer:
                next_layer.update(get_next_states_fast(config))
        else:
            with Pool(num_workers) as pool:
                results = pool.map(process_config, current_layer)
                for result in results:
                    next_layer.update(result)

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
    print()

    # Use iterative for now (parallel has overhead)
    values = solve_iterative(max_n)

    print("\nFinal values:")
    print("D =", values)
