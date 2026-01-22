#!/usr/bin/env python3
"""
Find a holonomic recurrence for D(n).
A holonomic recurrence has the form:
sum_{i=0}^{order} p_i(n) * D(n-i) = 0
where p_i(n) are polynomials in n.
"""

from fractions import Fraction
import numpy as np
from numpy.linalg import matrix_rank

# Known values
D = [1, 1, 3, 9, 30, 99, 336, 1134, 3855, 13086, 44499, 151263, 514419, 1749267]

def find_holonomic_recurrence(D, order, degree):
    """
    Try to find a recurrence of the form:
    sum_{i=0}^{order} (sum_{j=0}^{degree} c_{i,j} * n^j) * D(n-i) = 0

    Returns the coefficients c if found, None otherwise.
    """
    n_terms = len(D)
    n_unknowns = (order + 1) * (degree + 1)
    n_equations = n_terms - order

    if n_equations < n_unknowns:
        return None

    # Build the matrix A where each row corresponds to n = order, order+1, ...
    A = []
    for n in range(order, n_terms):
        row = []
        for i in range(order + 1):
            for j in range(degree + 1):
                # Coefficient of c_{i,j} is n^j * D(n-i)
                row.append(Fraction(n ** j) * Fraction(D[n - i]))
        A.append(row)

    # Convert to numpy for analysis
    A_np = np.array([[float(x) for x in row] for row in A])

    # Check rank - if rank < n_unknowns, there's a non-trivial solution
    r = matrix_rank(A_np, tol=1e-10)

    if r < n_unknowns:
        print(f"  Order {order}, degree {degree}: rank {r} < {n_unknowns} (potential solution)")

        # Use SVD to find null space
        U, S, Vh = np.linalg.svd(A_np)
        null_space = Vh[r:].T  # Null space vectors

        if null_space.shape[1] > 0:
            # Get the first null space vector
            coeffs = null_space[:, 0]

            # Normalize (divide by first non-zero)
            for c in coeffs:
                if abs(c) > 1e-10:
                    coeffs = coeffs / c
                    break

            # Reshape into (order+1) x (degree+1) matrix
            c_matrix = coeffs.reshape(order + 1, degree + 1)

            return c_matrix

    return None

def verify_recurrence(D, order, degree, coeffs):
    """Verify that the recurrence holds for all known terms."""
    for n in range(order, len(D)):
        val = 0
        for i in range(order + 1):
            poly_val = sum(coeffs[i, j] * (n ** j) for j in range(degree + 1))
            val += poly_val * D[n - i]
        if abs(val) > 1e-6:
            return False, n, val
    return True, None, None

print("Searching for holonomic recurrence...")
print(f"Using {len(D)} terms: D = {D}")
print()

for order in range(2, 6):
    for degree in range(1, 5):
        coeffs = find_holonomic_recurrence(D, order, degree)
        if coeffs is not None:
            print(f"\nPotential recurrence found: order={order}, degree={degree}")
            print("Coefficients (rows = lag i, cols = power j):")
            print(coeffs)

            ok, n, val = verify_recurrence(D, order, degree, coeffs)
            if ok:
                print("Verification: PASSED")

                # Print the recurrence in human-readable form
                print("\nRecurrence:")
                terms = []
                for i in range(order + 1):
                    poly_terms = []
                    for j in range(degree + 1):
                        c = coeffs[i, j]
                        if abs(c) > 1e-10:
                            if j == 0:
                                poly_terms.append(f"{c:.6f}")
                            elif j == 1:
                                poly_terms.append(f"{c:.6f}*n")
                            else:
                                poly_terms.append(f"{c:.6f}*n^{j}")
                    if poly_terms:
                        poly_str = " + ".join(poly_terms)
                        terms.append(f"({poly_str}) * D(n-{i})")
                print(" + ".join(terms) + " = 0")
            else:
                print(f"Verification: FAILED at n={n}, residual={val}")
            print()

# Also check for simpler recurrences of the form:
# D(n) = (an + b) * D(n-1) / c + (dn + e) * D(n-2) / f
print("\n\nChecking for simple 2-term recurrence:")
print("D(n) = a(n) * D(n-1) + b(n) * D(n-2)")
print()
for n in range(2, len(D)):
    # D(n) = a * D(n-1) + b * D(n-2)
    denom = D[n-1] * D[n-3] - D[n-2] ** 2 if n >= 3 else 1
    if denom != 0 and n >= 3:
        a = Fraction(D[n] * D[n-3] - D[n-1] * D[n-2], denom)
        b = (Fraction(D[n]) - a * Fraction(D[n-1])) / Fraction(D[n-2])
        print(f"n={n}: D({n}) = {float(a):.6f} * D({n-1}) + {float(b):.6f} * D({n-2})")
        print(f"       Check: {float(a) * D[n-1] + float(b) * D[n-2]:.2f} vs {D[n]}")
        print(f"       a = {a}, b = {b}")
