from heuristics import mrv, lcv
from ac3 import ac3
from utils import parse_landscape_line, read_input
from constants import masks, type_names, categories


def solve_csp(N, landscape, tile_counts, targets):
    k = N // 4  # Number of tiles per side (e.g., 5 for 20x20)
    if sum(tile_counts.values()) != k * k:
        raise ValueError(f"Tile counts sum to {sum(tile_counts.values())}, expected {k * k}")

    remaining = tile_counts.copy()
    variables = [(i, j) for i in range(k) for j in range(k)]
    domains = {var: set(range(3)) for var in variables}  # 0: FULL_BLOCK, 1: OUTER_BOUNDARY, 2: EL_SHAPE
    assignment = {}

    # Calculate total bushes in the landscape for validation
    total_bushes = [sum(row.count(i + 1) for row in landscape) for i in range(4)]

    def get_visible(assignment):
        covered = [[0] * N for _ in range(N)]
        for (i, j), t in assignment.items():
            mask = masks[t]
            for a in range(4):
                for b in range(4):
                    covered[i*4 + a][j*4 + b] |= mask[a][b]
        counts = [0] * 4
        for i in range(N):
            for j in range(N):
                if landscape[i][j] > 0 and not covered[i][j]:
                    counts[landscape[i][j] - 1] += 1
        return counts

    def backtrack():
        if len(assignment) == len(variables):
            visible = get_visible(assignment)
            return visible == [targets.get(i + 1, 0) for i in range(4)]

        var = mrv(variables, domains, assignment)
        if var is None:
            return False

        for val in lcv(var, domains, variables, assignment):
            cat = categories[val]
            if remaining[cat] > 0:
                assignment[var] = val
                remaining[cat] -= 1
                old_domains = {v: domains[v].copy() for v in variables}

                # Propagate constraints with AC-3
                if ac3(var, val, domains, variables, assignment):
                    if backtrack():
                        return True

                # Backtrack
                assignment.pop(var)
                remaining[cat] += 1
                for v in domains:
                    domains[v] = old_domains[v]
        return False

    # Initial AC-3 to enforce consistency before search (optional, can be skipped for simplicity)
    if not ac3(None, None, domains, variables, {}):
        print("No solution possible after initial constraint propagation")
        return

    if backtrack():
        print("Solution found:")
        for idx, (var, t) in enumerate(sorted(assignment.items(), key=lambda x: x[0][0] * k + x[0][1])):
            print(f"{idx} 4 {type_names[t]}")
        uncovered_counts = get_visible(assignment)
        print("\nUncovered Counts:")
        for i, count in enumerate(uncovered_counts):
            print(f"{i + 1}:{count}")
        return True
    else:
        print("No solution found")
        return False