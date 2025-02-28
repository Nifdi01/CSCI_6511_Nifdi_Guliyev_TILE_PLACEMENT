from ConstraintProp import ConstraintProp
from Node import Node
from Heuristic import Heuristic
from Tile import Tile
from Layouts import Layouts

def csp_alg(tiles, targets, tile_count, total_tiles):
    """
    CSP algorithm:
      - Create an ordered tile array (each tile initialized with a FULL layout).
      - Create the starting Node.
      - Maintain an open list and closed list.
      - Use MRV to choose the next node; if a solution is found (final_check passes),
        print the solution; otherwise, generate neighbors via LCV and AC3 consistency.
    Returns 0 if a solution is found, -1 otherwise.
    """
    cp = ConstraintProp()

    # Create tile array with each tile initialized with FULL layout.
    tile_array = []
    for i in range(total_tiles):
        tile_array.append(Tile(tiles[i], Layouts.getInitialLayout(), "FULL"))

    start = Node(tile_array, targets, tile_count)
    open_list = [start]
    closed_list = []

    while open_list:
        # Use MRV heuristic to select index of best node.
        index = Heuristic.mrv_calc(open_list)
        current = open_list.pop(index)
        closed_list.append(current)

        # If the current node is a solution, print and return.
        if current.final_check():
            solution_print(current)
            return 0

        # Generate neighbors using LCV heuristic.
        neighbors = get_neighbors(current)

        # Enforce arc consistency before adding neighbors.
        if cp.AC3(neighbors):
            for test in neighbors:
                if not in_closed(test, closed_list) and not in_open(test, open_list):
                    open_list.append(test)
                else:
                    test.parent = current

    return -1

def get_neighbors(current):
    """
    Generate and return the neighbor list for a given Node.
    Uses the tile_order() method to order tiles.
    For each tile, a new neighbor is created (copy of current),
    the best layout option is determined via LCV, and the layout is changed.
    If the neighbor isn’t already in the list—and it passes arc consistency—it’s added.
    """
    neighbors = []
    tile_order_list = current.tile_order()  # Returns list of [tile_index, count] pairs.
    for i in range(len(current.tiles)):
        # Create a deep copy using the Node copy constructor.
        neighbor = Node.from_node(current)
        # Use LCV heuristic on the tile indicated by tile_order_list[i][0]
        layout = Heuristic.lcv_calc(neighbor, tile_order_list[i][0])
        # Change layout based on the returned value:
        if layout == 0:
            neighbor.change_layout(tile_order_list[i][0], 1, 0)  # EL 0
        elif layout == 1:
            neighbor.change_layout(tile_order_list[i][0], 1, 1)  # EL 1
        elif layout == 2:
            neighbor.change_layout(tile_order_list[i][0], 1, 2)  # EL 2
        elif layout == 3:
            neighbor.change_layout(tile_order_list[i][0], 1, 3)  # EL 3
        elif layout == 4:
            neighbor.change_layout(tile_order_list[i][0], 0, 0)  # Outer
        elif layout == 5:
            neighbor.change_layout(tile_order_list[i][0], 2, 0)  # Full

        # Add neighbor if it is not already in the list.
        if neighbor not in neighbors:
            neighbors.append(neighbor)
            neighbor.parent = current
            if ConstraintProp.arc_consistency(neighbor):
                neighbors.remove(neighbor)
    return neighbors

def solution_print(current):
    """
    Prints the solution:
      - For each tile, prints its index and layout name.
      - Prints current layout and color counts.
    """
    out_str = ""
    for i, tile in enumerate(current.tiles):
        out_str += f"{i}: {tile.layoutName}\n"
    out_str += "Layout Count: " + str(current.currentLayoutCount) + "\n"
    out_str += "Color Count: " + str(current.currentColorCount)
    print(out_str)

def in_open(node, open_list):
    return node in open_list

def in_closed(node, closed_list):
    return node in closed_list
