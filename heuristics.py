from collections import defaultdict

def mrv(variables, domains, assignment):
    unassigned = [v for v in variables if v not in assignment]
    min_domain = float('inf')
    best_vars = []
    for v in unassigned:
        if len(domains[v]) < min_domain:
            min_domain = len(domains[v])
            best_vars = [v]
        elif len(domains[v]) == min_domain:
            best_vars.append(v)
    
    # Tie-breaking: Choose the variable involved in the most constraints
    max_constraints = -1
    best_var = None
    for v in best_vars:
        num_constraints = sum([1 for other in variables if other != v])  # All other variables are constraints
        if num_constraints > max_constraints:
            max_constraints = num_constraints
            best_var = v
    return best_var


def lcv(var, domains, variables, assignment):
    value_constraints = defaultdict(int)
    for value in domains[var]:
        temp_assignment = assignment.copy()
        temp_assignment[var] = value
        for other in variables:
            if other not in temp_assignment and value in domains[other]:
                value_constraints[value] += 1
    return sorted(domains[var], key=lambda val: value_constraints[val])
