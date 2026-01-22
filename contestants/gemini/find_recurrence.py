
import numpy as np

def find_linear_recurrence(sequence, max_order=10):
    seq = np.array(sequence, dtype=object)
    n = len(seq)
    
    for start_index in range(4): # Try skipping 0, 1, 2, 3 terms
        current_seq = seq[start_index:]
        m = len(current_seq)
        
        for order in range(1, min(max_order + 1, m // 2)):
            # We need at least 'order' equations (rows).
            # Each equation uses 'order+1' terms: a[k], a[k-1]... a[k-order]
            # k ranges from order to m-1.
            # Number of equations = m - order.
            # We need m - order >= order => m >= 2*order.
            
            # Construct Matrix A and vector b
            # A * c = b
            # A[i] = [a[order+i-1], a[order+i-2], ..., a[i]]
            # b[i] = a[order+i]
            
            num_equations = m - order
            if num_equations < order:
                continue
                
            A = []
            b = []
            for i in range(num_equations):
                row = [current_seq[order + i - j] for j in range(1, order + 1)]
                A.append(row)
                b.append(current_seq[order + i])
            
            A = np.array(A, dtype=float)
            b = np.array(b, dtype=float)
            
            # Solve using least squares
            try:
                x, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
                
                if residuals.size > 0 and residuals[0] > 1e-4:
                    continue
                
                # Check if x is close to integer
                x_rounded = np.round(x)
                if not np.allclose(x, x_rounded, atol=1e-4):
                    continue
                
                coeffs = x_rounded.astype(int)
                
                # Verify exactly
                valid = True
                for i in range(num_equations):
                    lhs = 0
                    for j in range(order):
                        lhs += coeffs[j] * current_seq[order + i - (j + 1)]
                    if lhs != current_seq[order + i]:
                        valid = False
                        break
                
                if valid:
                    return start_index, coeffs
                    
            except Exception as e:
                continue
                
    return None, None

sequence = [
    1, 1, 3, 9, 30, 99, 336, 1134, 3855, 13086, 
    44499, 151263, 514419, 1749267, 5949063, 20231571
]

start_idx, coeffs = find_linear_recurrence(sequence, max_order=8)

if coeffs is not None:
    print(f"Found recurrence starting at index {start_idx} (term {sequence[start_idx]}).")
    print(f"Order: {len(coeffs)}")
    print(f"Coefficients: {list(coeffs)}")
    # a[n] = c[0]*a[n-1] + c[1]*a[n-2] + ...
else:
    print("No linear recurrence found.")
