# Tile Placement
## Main CSP Class
The [`csp_solver.py`](csp_solver.py ) file contains the main implementation of the Constraint Satisfaction Problem (CSP) solver for the tile placement problem. This file defines the `LandscapeCSPSolver` class, which is responsible for managing the CSP, applying heuristics, and solving the problem using backtracking search with constraint propagation.

### Class: `LandscapeCSPSolver`

#### `__init__(self, N, landscape, tile_counts, targets)`

- **Parameters**:
  - `N`: The size of the landscape grid (N x N).
  - `landscape`: The landscape grid represented as a list of lists.
  - `tile_counts`: A dictionary specifying the count of each tile type.
  - `targets`: A dictionary specifying the target visibility requirements for different colored cells.

- **Initialization**:
  - Initializes various attributes such as `N`, `landscape`, `tile_counts`, `targets`, and `k` (number of tiles per side).
  - Validates the total number of tiles.
  - Initializes the remaining tile counts, variables (grid positions), and domains (possible tile types for each variable).
  - Initializes the AC-3 constraint propagator.
  - Calculates the total bushes in the landscape for validation.

#### `get_visible(self, assignment)`

- **Purpose**:
  - Calculates the number of visible bushes that are not covered by any tiles based on the current assignment.

- **Implementation**:
  - Initializes a `covered` grid to track covered cells.
  - Iterates through the assignment and applies the corresponding tile masks to the `covered` grid.
  - Counts the number of uncovered bushes for each color and returns the counts.

#### `backtrack(self)`

- **Purpose**:
  - Performs backtracking search with MRV (Minimum Remaining Values) and LCV (Least Constraining Value) heuristics to find a solution.

- **Implementation**:
  - Checks if the assignment is complete and validates the visibility requirements.
  - Selects the next variable to assign using the MRV heuristic.
  - Iterates through the possible values for the selected variable using the LCV heuristic.
  - Updates the assignment and remaining tile counts.
  - Propagates constraints using the AC-3 algorithm.
  - Recursively calls `backtrack` to continue the search.
  - If a solution is found, returns `True`; otherwise, backtracks and restores the previous state.

#### `solve(self)`

- **Purpose**:
  - The main solving method that initiates the CSP solving process.

- **Implementation**:
  - Performs initial constraint propagation using the AC-3 algorithm.
  - Calls the `backtrack` method to start the search.
  - Prints the solution and uncovered counts if a solution is found.
  - Returns `True` if a solution is found, otherwise returns `False`.

## AC3 Algorithm
The [`ac3.py`](ac3.py ) file contains the implementation of the AC-3 (Arc Consistency 3) algorithm, which is used for constraint propagation in Constraint Satisfaction Problems (CSPs). The AC-3 algorithm helps in reducing the search space by enforcing arc consistency, which means that for every variable, every value in its domain satisfies the variable's binary constraints.

### Class: `AC3ConstraintPropagator`

#### `__init__(self, variables)`

- **Parameters**:
  - `variables`: A list of variables in the CSP.

- **Initialization**:
  - Initializes the `variables` attribute with the provided list of variables.

#### `revise(self, x, y, domains, assignment)`

- **Purpose**:
  - Revises the domain of variable `x` with respect to variable `y`.
  - Returns `True` if the domain of `x` was reduced, indicating that some values were removed from `x`'s domain.

- **Implementation**:
  - Initializes a `revised` flag to `False` and a set `to_remove` to keep track of values to be removed from `x`'s domain.
  - Checks the current assignments of `x` and `y`:
    - If `x` is assigned, it checks for consistency with `y`'s domain.
    - If `y` is assigned, it checks for consistency with `x`'s domain.
    - If neither is assigned, it ensures that the domains allow different values.
  - If `x` is assigned, no revision is needed.
  - Removes the inconsistent values from `x`'s domain and sets the `revised` flag to `True` if any values were removed.
  - Returns the `revised` flag.

#### `propagate(self, var, val, domains, assignment)`

- **Purpose**:
  - Enforces arc consistency on the constraint network.
  - Returns `False` if inconsistency is detected, `True` otherwise.

- **Implementation**:
  - Initializes a queue of arcs to be checked for consistency.
  - If called with a new assignment (`var` is not `None`), it only propagates from the affected arcs.
  - If called initially (`var` is `None`), it adds all arcs to the queue.
  - While the queue is not empty:
    - Dequeues an arc `(x, y)` and calls `revise(x, y, domains, assignment)`.
    - If the domain of `x` is empty after revision, it returns `False` indicating inconsistency.
    - If the domain of `x` was revised, it adds the neighbors of `x` back to the queue for further propagation.
  - Returns `True` if no inconsistency is detected.

## Heuristics Class
The [`heuristics.py`](heuristics.py ) file contains the implementation of heuristic functions used in the CSP solver to improve the efficiency of the search process. Specifically, it includes the Minimum Remaining Values (MRV) heuristic and the Least Constraining Value (LCV) heuristic.

### Functions

#### `mrv(variables, domains, assignment)`

- **Purpose**:
  - Selects the next variable to assign using the Minimum Remaining Values (MRV) heuristic.
  - The MRV heuristic chooses the variable with the fewest legal values remaining in its domain, which helps to reduce the branching factor of the search tree.

- **Parameters**:
  - `variables`: A list of all variables in the CSP.
  - `domains`: A dictionary mapping each variable to its domain of possible values.
  - `assignment`: A dictionary representing the current partial assignment of variables.

- **Implementation**:
  - Filters out the assigned variables to get the list of unassigned variables.
  - Finds the variable(s) with the smallest domain size.
  - If there is a tie (multiple variables with the same smallest domain size), it breaks the tie by selecting the variable with the most unassigned neighbors.
  - Returns the selected variable.

#### `lcv(var, domains, variables, assignment)`

- **Purpose**:
  - Orders the values for a given variable using the Least Constraining Value (LCV) heuristic.
  - The LCV heuristic prefers values that rule out the fewest choices for the neighboring variables, which helps to keep the search space as large as possible.

- **Parameters**:
  - `var`: The variable for which to order the values.
  - `domains`: A dictionary mapping each variable to its domain of possible values.
  - `variables`: A list of all variables in the CSP.
  - `assignment`: A dictionary representing the current partial assignment of variables.

- **Implementation**:
  - Identifies the unassigned neighbors of the given variable.
  - For each value in the domain of the variable, counts how many values it rules out in the domains of the neighboring variables.
  - Sorts the values by the number of constraints they impose, preferring values that impose fewer constraints.
  - Returns the sorted list of values.

## Utils
The [`utils.py`](utils.py ) file contains utility functions that assist in parsing input files, processing landscape lines, and retrieving neighboring variables. These functions are essential for preparing the input data and supporting the CSP solver's operations.

### Functions

#### `parse_landscape_line(line, cell_width=2)`

- **Purpose**:
  - Processes a fixed-width line representing a row in the landscape grid.
  - Converts each cell in the row to an integer, with empty cells represented as 0.

- **Parameters**:
  - `line`: A string representing a row in the landscape grid.
  - `cell_width`: The width of each cell in the row (default is 2).

- **Implementation**:
  - Pads the line to ensure its length is a multiple of `cell_width`.
  - Slices the line into chunks of `cell_width`, strips each chunk, and converts nonempty chunks to integers.
  - Appends 0 for empty cells.
  - Returns a list of integers representing the row.


#### `read_input(filename)`

- **Purpose**:
  - Reads and parses the input file to extract the landscape grid, tile counts, and target visibility requirements.

- **Parameters**:
  - `filename`: The path to the input file.

- **Implementation**:
  - Opens the file and reads lines while keeping trailing spaces and ignoring empty lines.
  - Identifies the indices for the sections (`# Landscape`, `# Tiles:`, `# Targets:`).
  - Parses the landscape lines into a grid of integers.
  - Ensures the grid is square and its dimensions are divisible by 4.
  - Parses the tile counts and target visibility requirements.
  - Returns the grid dimension (`N`), landscape grid, tile counts, and targets.

#### `get_neighbors(var, variables)`

- **Purpose**:
  - Retrieves the neighboring variables of a given variable in the grid.

- **Parameters**:
  - `var`: The variable for which to find neighbors (a tuple representing grid coordinates).
  - `variables`: A list of all variables in the CSP.

- **Implementation**:
  - Calculates the grid size (`k`) based on the number of variables.
  - Identifies the neighboring variables (up, down, left, right) within the grid boundaries.
  - Returns a list of neighboring variables.