#!/usr/bin/env python3
"""
Dynamic programming approach based on the level-by-level structure.

At each level L (cells with x+y+z = L), cells are grouped by k = x+y.
Group G_{L,k} contains cells (i, k-i, L-k) for i = 0, 1, ..., k.
Constraint: at most one cell per group can be in D.

Cells that share a common child differ by (±1,∓1,0), etc.
Two cells are in the same group iff they have the same x+y value at the same level.

The key insight: at each level, we choose which groups have a cell in D.
Within each group, we choose which specific cell.
Connectivity: each cell at level L>0 must have a parent in D at level L-1.

Parents of cell (i, k-i, L-k) at level L in group k:
- (i-1, k-i, L-k) at L-1, group k-1 (if i > 0)
- (i, k-i-1, L-k) at L-1, group k-1 (if k-i > 0)
- (i, k-i, L-k-1) at L-1, group k (if L-k > 0)

So parents are in groups k-1 and/or k at level L-1.
"""

from collections import defaultdict
from functools import lru_cache

def compute_D_small(max_n):
    """Compute D(n) using a profile-based DP."""

    # Profile at level L: for each group k (0 to L), record if a cell is chosen
    # and which one (0 to k, or None for no cell).
    # This is exponential in L but let's try for small cases.

    # Actually, let's think about this differently.
    # The "profile" can be encoded more compactly.

    # At level L, groups are 0, 1, ..., L.
    # Each group k has k+1 cells.
    # We need to track which cells are in D to check connectivity for level L+1.

    # Let's use a different state representation:
    # At each level, the state is a tuple indicating which cells were chosen.
    # State = tuple of (group, cell_index) pairs, or None.

    # This is still exponential, but let's try.

    # Level 0: only one cell (0,0,0)
    # State: (0, 0) means cell (0, 0, 0) is in D

    # We track: for each level, a dict mapping (state at level L-1) -> count

    # At level 0:
    # - Either (0,0,0) is in D or not
    # - If n=0, we need exactly 0 divisions, so D is empty, one configuration
    # - If n≥1, (0,0,0) must be in D

    # Let's enumerate states differently.
    # State = frozenset of (group_index, cell_within_group)

    # Actually, let me just enumerate configurations directly for small n.

    return None

def analyze_structure():
    """Analyze the mathematical structure of valid configurations."""

    # Let's think about what the configurations look like.
    # At level 0: (0,0,0)
    # At level 1: (1,0,0), (0,1,0), (0,0,1)
    #   - Group 0: (0,0,1)
    #   - Group 1: (1,0,0), (0,1,0)

    # At level 2:
    #   - Group 0: (0,0,2)
    #   - Group 1: (1,0,1), (0,1,1)
    #   - Group 2: (2,0,0), (1,1,0), (0,2,0)

    # A configuration is specified by:
    # - Which levels have cells in D
    # - At each level, which groups have a cell
    # - Within each group, which cell

    # The constraints are:
    # 1. At most one cell per group
    # 2. Connectivity: each cell (except origin) has a parent in D

    # The number of groups at level L is L+1.
    # The number of cells at level L is (L+1)(L+2)/2.

    # Let's think about this as a lattice path problem.
    # Maybe the "profile" of which groups are filled can be described by a path.

    print("Structure analysis:")
    for L in range(5):
        print(f"\nLevel {L}:")
        for k in range(L + 1):
            cells = [(i, k - i, L - k) for i in range(k + 1)]
            print(f"  Group {k}: {cells}")

    # Key observation:
    # At level L, if we choose a cell in group k, its parents are in groups k-1 and k at level L-1.
    # So the "active" groups at level L depend on the active groups at level L-1.

    # This is like a "spreading" process: active groups can spawn cells in adjacent groups.

    # Let's define:
    # - active[L] = set of groups at level L that have a cell in D
    # - For connectivity, if k is in active[L] (for L > 0), then k-1 or k must be in active[L-1]
    #   (since the cell in group k has parents in groups k-1 and k)

    # Wait, that's not quite right. The cell choice within a group matters.

    # Let me think about edge cases:
    # - Cell (0, k, L-k) in group k at level L:
    #   - Parents: (0, k-1, L-k) in group k-1 at L-1 (if k > 0)
    #   - Parents: (0, k, L-k-1) in group k at L-1 (if L > k)
    # - Cell (k, 0, L-k) in group k at level L:
    #   - Parents: (k-1, 0, L-k) in group k-1 at L-1 (if k > 0)
    #   - Parents: (k, 0, L-k-1) in group k at L-1 (if L > k)
    # - Cell (i, k-i, L-k) with 0 < i < k:
    #   - Parents: (i-1, k-i, L-k) in group k-1 at L-1
    #   - Parents: (i, k-i-1, L-k) in group k-1 at L-1
    #   - Parents: (i, k-i, L-k-1) in group k at L-1 (if L > k)

    # So:
    # - Edge cells (i=0 or i=k) can have parents in groups k-1 and/or k
    # - Middle cells (0 < i < k) have parents in groups k-1 and k (if L > k)

    # For middle cells, connectivity is satisfied if either k-1 or k is active at L-1.
    # For edge cells, it depends on which specific cell is chosen.

    print("\n\nParent structure:")
    for L in range(1, 4):
        print(f"\nLevel {L}:")
        for k in range(L + 1):
            for i in range(k + 1):
                cell = (i, k - i, L - k)
                parents = []
                if i > 0:
                    parents.append(f"({i-1}, {k-i}, {L-k}) in G{k-1}")
                if k - i > 0:
                    parents.append(f"({i}, {k-i-1}, {L-k}) in G{k-1}")
                if L - k > 0:
                    parents.append(f"({i}, {k-i}, {L-k-1}) in G{k}")
                print(f"  Cell {cell} in G{k}: parents = {parents}")

if __name__ == "__main__":
    analyze_structure()
