from collections import defaultdict
from utils import get_neighbors

def mrv(variables, domains, assignment):
    unassigned = [v for v in variables if v not in assignment]
    if not unassigned:
        return None
    min_domain = float('inf')
    best_vars = []
    for v in unassigned:
        domain_size = len(domains[v])
        if domain_size < min_domain:
            min_domain = domain_size
            best_vars = [v]
        elif domain_size == min_domain:
            best_vars.append(v)
    
    if len(best_vars) == 1:
        return best_vars[0]
    
    # Tie-breaking: Choose variable with most unassigned neighbors
    max_neighbors = -1
    best_var = None
    for v in best_vars:
        neighbors = [n for n in get_neighbors(v, variables) if n not in assignment]
        num_neighbors = len(neighbors)
        if num_neighbors > max_neighbors:
            max_neighbors = num_neighbors
            best_var = v
    return best_var

def lcv(var, domains, variables, assignment):
    neighbors = [n for n in get_neighbors(var, variables) if n not in assignment]
    value_constraints = defaultdict(int)
    for value in domains[var]:
        # Count how many values this assignment rules out in neighbors
        for neighbor in neighbors:
            if value in domains[neighbor]:
                value_constraints[value] += 1
    # Sort by least constraining (fewer values ruled out)
    return sorted(domains[var], key=lambda val: value_constraints[val])