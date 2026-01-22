#!/usr/bin/env python3
"""
Solve the 2D version of the amoeba problem to gain insights.

In 2D: amoeba at (x,y) divides into (x+1,y) and (x,y+1) if both empty.
After N divisions: N+1 amoebas.
"""

def get_next_states_2d(config):
    """Generate all states reachable by one division in 2D."""
    next_states = set()
    for (x, y) in config:
        c1 = (x + 1, y)
        c2 = (x, y + 1)
        if c1 not in config and c2 not in config:
            new_config = set(config)
            new_config.remove((x, y))
            new_config.add(c1)
            new_config.add(c2)
            next_states.add(frozenset(new_config))
    return next_states

def compute_D2(max_n):
    """Compute D2(n) for 2D problem."""
    current_layer = {frozenset([(0, 0)])}
    values = [1]

    for n in range(1, max_n + 1):
        next_layer = set()
        for config in current_layer:
            next_layer.update(get_next_states_2d(config))
        current_layer = next_layer
        values.append(len(current_layer))
        print(f"D2({n}) = {len(current_layer)}")

    return values

def catalan(n):
    """Compute the nth Catalan number."""
    if n <= 0:
        return 1
    result = 1
    for i in range(n):
        result = result * (2 * n - i) // (i + 1)
    return result // (n + 1)

print("2D Amoeba problem:")
D2 = compute_D2(15)

print("\nComparing with Catalan numbers:")
print("n\tD2(n)\tC(n)\tC(n-1)")
for n in range(len(D2)):
    c_n = catalan(n)
    c_n_minus_1 = catalan(n - 1) if n > 0 else 1
    print(f"{n}\t{D2[n]}\t{c_n}\t{c_n_minus_1}")

# The 2D configurations are in bijection with certain lattice paths
print("\n\nAnalysis:")
print("Let's check if D2(n) = C(n) (Catalan numbers)...")
is_catalan = all(D2[n] == catalan(n) for n in range(len(D2)))
print(f"D2(n) = C(n): {is_catalan}")

print("\nLet's check if D2(n) = C(n-1)...")
is_catalan_shifted = all(D2[n] == catalan(n - 1) for n in range(1, len(D2)))
print(f"D2(n) = C(n-1) for n >= 1: {is_catalan_shifted}")

# Other formulas
print("\nChecking other formulas:")
from math import comb
for n in range(1, len(D2)):
    # Number of ways to place n 1s in a sequence of n positions
    # such that partial sums don't exceed the position
    # This is the ballot number / Catalan variant
    # Actually, this is the number of Dyck paths of semilength n

    # Let's check: D2(n) = choose(2n-2, n-1) / n for n >= 1
    if n >= 1:
        ballot = comb(2*n - 2, n - 1) // n if n > 0 else 1
        print(f"n={n}: D2(n)={D2[n]}, C(n-1)={catalan(n-1)}, ballot={ballot}")
