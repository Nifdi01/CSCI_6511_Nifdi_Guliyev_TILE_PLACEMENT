from collections import deque
from utils import get_neighbors


class AC3ConstraintPropagator:
    def __init__(self, variables):
        self.variables = variables
    
    def revise(self, x, y, domains, assignment):
        """
        Revise the domain of x with respect to y.
        Returns True if the domain of x was reduced.
        """
        revised = False
        to_remove = set()
        x_val = assignment.get(x)
        y_val = assignment.get(y)
        
        # If x is assigned, check consistency with y's domain
        if x_val is not None:
            for val_y in domains[y]:
                if val_y == x_val:  # Inequality constraint
                    to_remove.add(val_y)
        # If y is assigned, check consistency with x's domain
        elif y_val is not None:
            for val_x in domains[x]:
                if val_x == y_val:
                    to_remove.add(val_x)
        # If neither assigned, ensure domains allow different values
        else:
            for val_x in domains[x]:
                if all(val_x == val_y for val_y in domains[y]):
                    to_remove.add(val_x)
        
        if x in assignment:
            return False  # No revision needed for assigned variables
            
        domains[x] -= to_remove
        if to_remove:
            revised = True
        
        return revised
    
    def propagate(self, var, val, domains, assignment):
        """
        Enforce arc consistency on the constraint network.
        Returns False if inconsistency is detected, True otherwise.
        """
        # If called with a new assignment, only propagate from affected arcs
        if var is not None:
            queue = deque([(n, var) for n in get_neighbors(var, self.variables) if n not in assignment])
        else:
            # Initial call: all arcs
            queue = deque()
            for x in self.variables:
                for y in get_neighbors(x, self.variables):
                    if y > x:  # Avoid duplicates (e.g., (0,1) and (1,0))
                        queue.append((x, y))
    
        while queue:
            (x, y) = queue.popleft()
            if self.revise(x, y, domains, assignment):
                if not domains[x]:
                    return False  # Domain wipeout, inconsistency detected
                # Add neighbors of x back to the queue
                for z in get_neighbors(x, self.variables):
                    if z != y and z not in assignment:
                        queue.append((z, x))
        
        return True  # No inconsistency detected