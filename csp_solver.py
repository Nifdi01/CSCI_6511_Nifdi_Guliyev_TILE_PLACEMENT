from heuristics import mrv, lcv
from ac3 import AC3ConstraintPropagator
from utils import parse_landscape_line, read_input
from constants import masks, type_names, categories


class LandscapeCSPSolver:
    def __init__(self, N, landscape, tile_counts, targets):
        self.N = N
        self.landscape = landscape
        self.tile_counts = tile_counts
        self.targets = targets
        self.k = N // 4  # Number of tiles per side (for 20x20)
        
        if sum(tile_counts.values()) != self.k * self.k:
            raise ValueError(f"Tile counts sum to {sum(tile_counts.values())}, expected {self.k * self.k}")
        
        self.remaining = tile_counts.copy()
        self.variables = [(i, j) for i in range(self.k) for j in range(self.k)]
        self.ac3 = AC3ConstraintPropagator(self.variables)
        self.domains = {var: set(range(3)) for var in self.variables}  # 0: FULL_BLOCK, 1: OUTER_BOUNDARY, 2: EL_SHAPE
        self.assignment = {}
        
        # Calculate total bushes in the landscape for validation
        self.total_bushes = [sum(row.count(i + 1) for row in landscape) for i in range(4)]
    
    def get_visible(self, assignment):
        """Calculate visible bushes that aren't covered by any tiles"""
        covered = [[0] * self.N for _ in range(self.N)]
        
        for (i, j), t in assignment.items():
            mask = masks[t]
            for a in range(4):
                for b in range(4):
                    covered[i*4 + a][j*4 + b] |= mask[a][b]
        
        counts = [0] * 4
        for i in range(self.N):
            for j in range(self.N):
                if self.landscape[i][j] > 0 and not covered[i][j]:
                    counts[self.landscape[i][j] - 1] += 1
        
        return counts
    
    def backtrack(self):
        """Backtracking search with MRV and LCV heuristics"""
        if len(self.assignment) == len(self.variables):
            visible = self.get_visible(self.assignment)
            return visible == [self.targets.get(i + 1, 0) for i in range(4)]
        
        var = mrv(self.variables, self.domains, self.assignment)
        if var is None:
            return False
        
        for val in lcv(var, self.domains, self.variables, self.assignment):
            cat = categories[val]
            if self.remaining[cat] > 0:
                self.assignment[var] = val
                self.remaining[cat] -= 1
                old_domains = {v: self.domains[v].copy() for v in self.variables}
                
                # Propagate constraints with AC-3
                if self.ac3.propagate(var, val, self.domains, self.assignment):
                    if self.backtrack():
                        return True
                
                # Backtrack
                self.assignment.pop(var)
                self.remaining[cat] += 1
                for v in self.domains:
                    self.domains[v] = old_domains[v]
        
        return False
    
    def solve(self):
        """Main solving method"""
        # Initial AC-3 to enforce consistency before search
        if not self.ac3.propagate(None, None, self.domains, {}):
            print("No solution possible after initial constraint propagation")
            return False
        
        if self.backtrack():
            print("Solution found:")
            for idx, (var, t) in enumerate(sorted(self.assignment.items(), 
                                                  key=lambda x: x[0][0] * self.k + x[0][1])):
                print(f"{idx} 4 {type_names[t]}")
            
            uncovered_counts = self.get_visible(self.assignment)
            print("\nUncovered Counts:")
            for i, count in enumerate(uncovered_counts):
                print(f"{i + 1}:{count}")
            return True
        else:
            print("No solution found")
            return False