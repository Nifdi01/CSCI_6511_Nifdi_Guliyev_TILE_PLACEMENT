from collections import deque

def ac3(domains, variables):
    def get_neighbors(var):
        # Get adjacent variables (up, down, left, right)
        i, j = var
        neighbors = []
        if i > 0:
            neighbors.append((i-1, j))  # up
        if j > 0:
            neighbors.append((i, j-1))  # left
        if i < max(x[0] for x in variables):
            neighbors.append((i+1, j))  # down
        if j < max(x[1] for x in variables):
            neighbors.append((i, j+1))  # right
        return [n for n in neighbors if n in variables]

    # Initialize queue with only adjacent variables
    queue = deque()
    for var in variables:
        for neighbor in get_neighbors(var):
            queue.append((var, neighbor))

    def revise(x, y):
        revised = False
        to_remove = set()
        
        # Check tile compatibility between neighbors
        for val_x in domains[x]:
            # For this specific puzzle, we just need to ensure
            # adjacent tiles are different (or implement specific
            # tile compatibility rules if needed)
            if all(val_x == val_y for val_y in domains[y]):
                to_remove.add(val_x)
        
        if to_remove:
            domains[x] -= to_remove
            revised = True
        return revised

    while queue:
        (x, y) = queue.popleft()
        if revise(x, y):
            if not domains[x]:  # Empty domain means inconsistency
                return False
            # Only add neighbors of x back to queue
            for z in get_neighbors(x):
                if z != y:  # Avoid redundant checks
                    queue.append((z, x))
    return True