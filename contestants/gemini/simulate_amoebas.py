
def get_next_states(current_config):
    next_states = set()
    # current_config is a frozenset of (x, y, z) tuples
    for (x, y, z) in current_config:
        # Proposed new cells
        c1 = (x + 1, y, z)
        c2 = (x, y + 1, z)
        c3 = (x, y, z + 1)
        
        # Check if they are empty
        if c1 not in current_config and c2 not in current_config and c3 not in current_config:
            # Create new config
            new_config = set(current_config)
            new_config.remove((x, y, z))
            new_config.add(c1)
            new_config.add(c2)
            new_config.add(c3)
            next_states.add(frozenset(new_config))
    return next_states

def solve_small_n(max_n):
    current_layer = {frozenset([(0, 0, 0)])}
    print(f"D(0) = {len(current_layer)}")
    
    for n in range(1, max_n + 1):
        next_layer = set()
        for config in current_layer:
            next_layer.update(get_next_states(config))
        current_layer = next_layer
        print(f"D({n}) = {len(current_layer)}")

if __name__ == "__main__":
    solve_small_n(6)
