
def solve_recurrence_mod(sequence, mod, max_order=8):
    # Works in Z_p
    # Just brute force coefficients?
    # Or Gaussian elimination in Z_p.
    # For small mod, brute force is hard if order is large (mod^order).
    # Gaussian elimination is best.
    pass

# We'll just use a simple solver
def find_linear_recurrence_mod(sequence, mod, max_order=8):
    seq = [x % mod for x in sequence]
    n = len(seq)
    
    for start_index in range(3):
        curr_seq = seq[start_index:]
        m = len(curr_seq)
        
        for order in range(1, min(max_order + 1, m // 2)):
            # Build matrix A and b in Z_mod
            num_eq = m - order
            if num_eq < order: continue
            
            # We want to solve A * c = b (mod mod)
            # Iterate through all combinations? No.
            # Use Gaussian elimination over finite field.
            # Assuming mod is prime for simplicity of division (inverse).
            
            # Implementation of Gaussian elimination mod p
            rows = []
            for i in range(order): # Use first 'order' equations
                row = [curr_seq[order + i - j] for j in range(1, order + 1)] + [curr_seq[order + i]]
                rows.append(row)
            
            # Solve
            coeffs = gaussian_elimination_mod(rows, mod)
            
            if coeffs is not None:
                # Verify
                valid = True
                for i in range(num_eq):
                    lhs = sum(coeffs[j] * curr_seq[order + i - (j + 1)] for j in range(len(coeffs)))
                    lhs %= mod
                    if lhs != curr_seq[order + i]:
                        valid = False
                        break
                if valid:
                    return start_index, coeffs

    return None, None

def gaussian_elimination_mod(matrix, mod):
    # Matrix is augmented [A | b]
    # Returns solution x or None
    mat = [row[:] for row in matrix]
    rows = len(mat)
    cols = len(mat[0]) - 1 # variables
    
    if rows < cols: return None
    
    # Forward elimination
    pivot_row = 0
    for col in range(cols):
        if pivot_row >= rows: break
        
        # Find pivot
        idx = -1
        for r in range(pivot_row, rows):
            if mat[r][col] % mod != 0:
                idx = r
                break
        
        if idx == -1: continue # No pivot in this column
        
        # Swap
        mat[pivot_row], mat[idx] = mat[idx], mat[pivot_row]
        
        # Scale pivot to 1
        inv = pow(mat[pivot_row][col], mod - 2, mod) # Fermat's Little Theorem
        for c in range(col, cols + 1):
            mat[pivot_row][c] = (mat[pivot_row][c] * inv) % mod
            
        # Eliminate below
        for r in range(rows):
            if r != pivot_row:
                factor = mat[r][col]
                for c in range(col, cols + 1):
                    mat[r][c] = (mat[r][c] - factor * mat[pivot_row][c]) % mod
        
        pivot_row += 1
        
    # Extract solution
    # Check consistency
    # Assuming unique solution for now or just taking one
    res = [0] * cols
    for r in range(rows):
        # Find first non-zero
        first = -1
        for c in range(cols):
            if mat[r][c] != 0:
                first = c
                break
        
        if first == -1:
            if mat[r][cols] != 0: return None # Inconsistent
        else:
            res[first] = mat[r][cols]
            
    return res

sequence = [
    1, 1, 3, 9, 30, 99, 336, 1134, 3855, 13086, 
    44499, 151263, 514419, 1749267, 5949063, 20231571
]

# Try a few primes
for p in [1009, 10007, 100003]:
    start, coeffs = find_linear_recurrence_mod(sequence, p, max_order=8)
    if coeffs:
        print(f"Found recurrence mod {p}: order {len(coeffs)}, start {start}, coeffs {coeffs}")
