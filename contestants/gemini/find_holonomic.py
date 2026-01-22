
import numpy as np

def find_holonomic_recurrence(sequence, max_order=4, max_degree=3):
    seq = np.array(sequence, dtype=object)
    n = len(seq)
    
    # We want to find coeffs c_{i,j} such that:
    # sum_{i=0}^{order} sum_{j=0}^{degree} c_{i,j} * n^j * a_{n-i} = 0
    # valid for all n in range [order, len(seq)-1]
    
    # We normalize to n relative to the current equation index?
    # Let's say the equation holds for index k.
    # sum_{i=0}^{order} P_i(k) * a_{k-i} = 0
    # where P_i(k) is a polynomial of degree max_degree.
    
    # Total unknowns: (max_order + 1) * (max_degree + 1)
    # We set one coeff to 1 (normalization) to avoid trivial 0 solution?
    # Or just solve homogeneous system and look for null space.
    
    num_vars = (max_order + 1) * (max_degree + 1)
    
    equations = []
    
    # Generate equations for each valid k
    for k in range(max_order, n):
        row = []
        for i in range(max_order + 1): # term a_{k-i}
            term_val = seq[k-i]
            for j in range(max_degree + 1): # coeff of k^j
                row.append(term_val * (k**j))
        equations.append(row)
        
    if len(equations) < num_vars - 1:
        print(f"Not enough data for order={max_order}, degree={max_degree}")
        return None
        
    # Solve M * x = 0
    M = np.array(equations, dtype=float)
    
    # SVD to find null space
    try:
        U, S, Vh = np.linalg.svd(M)
        # The last row of Vh corresponds to the smallest singular value
        null_vec = Vh[-1]
        smallest_sv = S[-1] if len(S) > 0 else 0
        
        # If smallest singular value is small, we have a solution
        if smallest_sv > 1e-4:
            return None # No exact solution likely
            
        # Normalize and round
        # Find element with largest magnitude to normalize
        max_idx = np.argmax(np.abs(null_vec))
        null_vec /= null_vec[max_idx]
        
        x_rounded = np.round(null_vec)
        if not np.allclose(null_vec, x_rounded, atol=1e-3):
            return None
            
        coeffs = x_rounded.astype(int)
        return coeffs.reshape((max_order + 1, max_degree + 1))
        
    except Exception as e:
        print(e)
        return None

sequence = [
    1, 1, 3, 9, 30, 99, 336, 1134, 3855, 13086, 
    44499, 151263, 514419, 1749267, 5949063, 20231571
]

# Try various orders and degrees
for order in range(1, 5):
    for degree in range(0, 4):
        coeffs = find_holonomic_recurrence(sequence, max_order=order, max_degree=degree)
        if coeffs is not None:
            print(f"Found Holonomic Recurrence! Order={order}, Degree={degree}")
            print(coeffs)
            # Interpret coeffs
            # coeffs[i, j] corresponds to a_{n-i} * n^j
            # Note: n is the index in the sequence (0-based)
            exit()

print("No holonomic recurrence found.")
