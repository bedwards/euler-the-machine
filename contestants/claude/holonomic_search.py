#!/usr/bin/env python3
"""
Systematic search for a holonomic recurrence:
p_0(n)*D(n) + p_1(n)*D(n-1) + ... + p_r(n)*D(n-r) = 0
where p_i(n) are polynomials.
"""

from fractions import Fraction
from functools import reduce
from math import gcd

# Known values
D = [1, 1, 3, 9, 30, 99, 336, 1134, 3855, 13086, 44499, 151263, 514419, 1749267]

def lcm(a, b):
    return a * b // gcd(a, b)

def solve_linear_system(A, b):
    """Solve Ax = b using Gaussian elimination with fractions."""
    n = len(A)
    m = len(A[0])

    # Augmented matrix
    M = [row[:] + [b[i]] for i, row in enumerate(A)]

    # Forward elimination
    for col in range(min(n, m)):
        # Find pivot
        pivot_row = None
        for row in range(col, n):
            if M[row][col] != 0:
                pivot_row = row
                break

        if pivot_row is None:
            continue

        # Swap rows
        M[col], M[pivot_row] = M[pivot_row], M[col]

        # Eliminate
        for row in range(col + 1, n):
            if M[row][col] != 0:
                factor = M[row][col] / M[col][col]
                for j in range(col, m + 1):
                    M[row][j] -= factor * M[col][j]

    # Back substitution
    x = [Fraction(0)] * m
    for col in range(min(n, m) - 1, -1, -1):
        if M[col][col] != 0:
            val = M[col][m]
            for j in range(col + 1, m):
                val -= M[col][j] * x[j]
            x[col] = val / M[col][col]

    return x

def find_recurrence(D, order, degree):
    """
    Find coefficients for:
    sum_{i=0}^{order} (sum_{j=0}^{degree} c[i][j] * n^j) * D[n-i] = 0

    We normalize by setting c[0][degree] = 1 (coefficient of n^degree * D(n)).
    """
    n_terms = len(D)
    n_unknowns = (order + 1) * (degree + 1) - 1  # -1 for normalization
    n_equations = n_terms - order

    if n_equations < n_unknowns:
        return None

    # Build system: for each n from order to len(D)-1
    # sum over (i,j) of c[i][j] * n^j * D[n-i] = 0
    # Normalized: -n^degree * D(n) = sum of other terms

    A = []
    b = []
    for n in range(order, n_terms):
        row = []
        # Go through all (i,j) pairs except (0, degree) which we normalize
        for i in range(order + 1):
            for j in range(degree + 1):
                if i == 0 and j == degree:
                    continue  # This is our normalized coefficient
                row.append(Fraction(n ** j * D[n - i]))
        A.append(row)
        b.append(Fraction(-n ** degree * D[n]))  # RHS is -1 * normalized term

    # Solve the overdetermined system (if n_equations > n_unknowns, use least squares)
    # Actually, we want an exact solution, so check if the system is consistent

    if n_equations >= n_unknowns:
        x = solve_linear_system(A[:n_unknowns], b[:n_unknowns])

        # Verify with remaining equations
        all_ok = True
        for k in range(n_unknowns, min(n_equations, n_unknowns + 5)):
            val = sum(A[k][j] * x[j] for j in range(len(x)))
            if abs(val - b[k]) > Fraction(1, 10**10):
                all_ok = False
                break

        if all_ok:
            # Reconstruct coefficient matrix
            coeffs = {}
            idx = 0
            for i in range(order + 1):
                for j in range(degree + 1):
                    if i == 0 and j == degree:
                        coeffs[(i, j)] = Fraction(1)
                    else:
                        coeffs[(i, j)] = x[idx]
                        idx += 1
            return coeffs

    return None

def format_poly(coeffs, degree, var='n'):
    """Format a polynomial nicely."""
    terms = []
    for j in range(degree, -1, -1):
        c = coeffs.get(j, Fraction(0))
        if c == 0:
            continue
        if j == 0:
            terms.append(str(c))
        elif j == 1:
            if c == 1:
                terms.append(var)
            elif c == -1:
                terms.append(f"-{var}")
            else:
                terms.append(f"{c}*{var}")
        else:
            if c == 1:
                terms.append(f"{var}^{j}")
            elif c == -1:
                terms.append(f"-{var}^{j}")
            else:
                terms.append(f"{c}*{var}^{j}")
    return " + ".join(terms).replace(" + -", " - ") if terms else "0"

print("Searching for holonomic recurrence...")
print(f"Data: D = {D}")
print()

found = False
for order in range(2, 5):
    for degree in range(1, 4):
        coeffs = find_recurrence(D, order, degree)
        if coeffs is not None:
            print(f"Found recurrence with order={order}, degree={degree}")

            # Format nicely
            print("Recurrence: ", end="")
            terms = []
            for i in range(order + 1):
                poly_coeffs = {j: coeffs[(i, j)] for j in range(degree + 1)}
                poly_str = format_poly(poly_coeffs, degree)
                if poly_str != "0":
                    terms.append(f"({poly_str})*D(n-{i})")
            print(" + ".join(terms) + " = 0")
            print()

            # Print raw coefficients
            print("Coefficients c[i][j] (for n^j * D(n-i)):")
            for i in range(order + 1):
                row = [coeffs[(i, j)] for j in range(degree + 1)]
                print(f"  i={i}: {row}")
            print()

            # Verify
            print("Verification:")
            for n in range(order, len(D)):
                val = sum(coeffs[(i, j)] * n**j * D[n - i]
                          for i in range(order + 1)
                          for j in range(degree + 1))
                print(f"  n={n}: sum = {val}")
            print()

            # Find integer coefficients by multiplying by common denominator
            all_denoms = [coeffs[(i, j)].denominator
                         for i in range(order + 1)
                         for j in range(degree + 1)]
            common_denom = reduce(lcm, all_denoms)
            print(f"Common denominator: {common_denom}")
            print("Integer coefficients (multiply recurrence by common denom):")
            for i in range(order + 1):
                row = [int(coeffs[(i, j)] * common_denom) for j in range(degree + 1)]
                print(f"  i={i}: {row}")

            found = True
            break
    if found:
        break

if not found:
    print("No recurrence found with order ≤ 4 and degree ≤ 3")

# Also check growth rate
print("\n\nGrowth analysis:")
for n in range(1, len(D)):
    if D[n-1] > 0:
        ratio = D[n] / D[n-1]
        print(f"D({n})/D({n-1}) = {D[n]}/{D[n-1]} = {ratio:.6f}")
