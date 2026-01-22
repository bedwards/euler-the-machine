#!/usr/bin/env python3
"""
Analyze the sequence D(n) to find a recurrence relation.
"""

from fractions import Fraction

# Known values computed by brute force
D = [1, 1, 3, 9, 30, 99, 336, 1134, 3855, 13086, 44499, 151263]

# Check ratios
print("Ratios D(n)/D(n-1):")
for i in range(1, len(D)):
    print(f"  D({i})/D({i-1}) = {D[i]}/{D[i-1]} = {D[i]/D[i-1]:.6f}")

print("\nChecking for linear recurrence D(n) = a*D(n-1) + b*D(n-2):")
# This would require: D(n)/D(n-1) = a + b*D(n-2)/D(n-1)
# Let's see if this holds

print("\nLooking for recurrence: D(n) = (a*n + b)*D(n-1)/c + (d*n + e)*D(n-2)/f")
# Try to fit with rational coefficients

# Check specific formulas
print("\nChecking Fuss-Catalan: C(3n,n)/(2n+1)")
from math import comb
for n in range(len(D)):
    fc = comb(3*n, n) // (2*n + 1) if n > 0 else 1
    print(f"  n={n}: D({n})={D[n]}, FC={fc}, match={D[n]==fc}")

print("\nChecking other Catalan variants:")
for n in range(len(D)):
    # Try C(2n,n)/(n+1) = Catalan
    cat = comb(2*n, n) // (n + 1)
    # Try central trinomial
    trin = sum(comb(n, k) * comb(n, 2*k) for k in range(n//2 + 1)) if n > 0 else 1
    print(f"  n={n}: D={D[n]}, Cat={cat}, Trin={trin}")

# Try to find recurrence of the form: D(n) = sum of a_i(n) * D(n-i)
# where a_i(n) are rational functions of n

print("\nTrying to find recurrence with polynomial coefficients...")

def find_recurrence(D, max_order=4, max_degree=2):
    """Try to find a recurrence of the form:
    sum_{i=0}^{order} p_i(n) * D(n-i) = 0
    where p_i(n) are polynomials of degree <= max_degree
    """
    from fractions import Fraction

    n_vals = len(D)
    for order in range(2, max_order + 1):
        # Number of polynomial coefficients: (order+1) * (max_degree+1)
        n_unknowns = (order + 1) * (max_degree + 1)
        if n_vals - order < n_unknowns:
            continue

        # Build system of equations
        # For each n from order to n_vals-1:
        # sum_{i=0}^{order} (sum_{d=0}^{max_degree} c_{i,d} * n^d) * D(n-i) = 0

        # This is a linear system in c_{i,d}
        A = []
        for n in range(order, n_vals):
            row = []
            for i in range(order + 1):
                for d in range(max_degree + 1):
                    row.append(Fraction(n**d * D[n - i]))
            A.append(row)

        # Find null space (homogeneous solution)
        # Use Gaussian elimination
        if len(A) >= n_unknowns - 1:
            # Try to find a non-trivial solution
            # Assume p_0 coefficient of n^{max_degree} is 1 (normalization)
            # Then solve for other coefficients
            pass

    return None

# Try a different approach: check if D(n) / D(n-1) approaches a constant * n^alpha
print("\nChecking growth rate:")
for n in range(2, len(D)):
    r = D[n] / D[n-1]
    print(f"  n={n}: D({n})/D({n-1}) = {r:.6f}")

# Let's see if there's a pattern in consecutive differences
print("\nSecond-order analysis:")
for n in range(2, len(D)):
    # Check if D(n)*D(n-2) / D(n-1)^2 is constant
    ratio = D[n] * D[n-2] / (D[n-1] ** 2)
    print(f"  n={n}: D({n})*D({n-2})/D({n-1})^2 = {ratio:.6f}")

print("\nLooking for pattern: D(n) = sum of products involving factorials/binomials")
# The answer might involve a sum or product formula
