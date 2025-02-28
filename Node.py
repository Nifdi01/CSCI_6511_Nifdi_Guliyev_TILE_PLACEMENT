from Tile import Tile
from Layouts import Layouts

class Node:
    def __init__(self, tiles, target_num, tile_count):
        """
        Initialize a Node.
          - tiles: list of Tile objects.
          - target_num: list of four ints (goal bush color counts for '1', '2', '3', '4').
          - tile_count: list of three ints (goal layout counts in order [OUTER, EL, FULL]).
        """
        self.tiles = tiles
        self.layoutTarget = tile_count[:]   # Make a copy to avoid accidental modification
        self.colorTarget = target_num[:]      # Copy of color targets
        self.parent = None
        self.currentLayoutCount = self.layout_number_calc()
        self.currentColorCount = self.target_number_calc()
        self.distLayout = tile_count[0] + tile_count[1] + tile_count[2]
        self.distColor = sum(self.currentColorCount)

    @classmethod
    def from_node(cls, base):
        """
        Copy constructor: creates a new Node from an existing one.
        A deep copy of each Tile is created (assuming Tile.value and Tile.layout are lists).
        """
        new_tiles = []
        for tile in base.tiles:
            # Create a new Tile copying value, layout, and layoutName.
            new_tile = Tile(tile.value.copy(), tile.layout.copy(), tile.layoutName)
            new_tiles.append(new_tile)
        new_node = cls(new_tiles, base.colorTarget, base.layoutTarget)
        new_node.parent = base
        new_node.currentLayoutCount = new_node.layout_number_calc()
        new_node.currentColorCount = new_node.target_number_calc()
        new_node.distColor = base.distColor
        new_node.distLayout = base.distLayout
        return new_node

    def layout_number_calc(self):
        """
        Count how many tiles are assigned to each layout.
          Index 0: OUTER
          Index 1: any of the EL layouts ("EL 0", "EL 1", "EL 2", "EL 3")
          Index 2: FULL
        Returns a list of three counts.
        """
        num_calc = [0, 0, 0]
        for tile in self.tiles:
            if tile.layoutName == "OUTER":
                num_calc[0] += 1
            if tile.layoutName in {"EL 0", "EL 1", "EL 2", "EL 3"}:
                num_calc[1] += 1
            if tile.layoutName == "FULL":
                num_calc[2] += 1
        return num_calc

    def target_number_calc(self):
        """
        Count how many bush colors (represented by characters '1','2','3','4') are uncovered.
        A bush is counted only if tile.value[j] is one of '1','2','3','4'
        and the corresponding tile.layout[j] is '0'.
        Returns a list of four counts [one, two, three, four].
        """
        one = two = three = four = 0
        for tile in self.tiles:
            for j in range(len(tile.value)):
                if tile.value[j] == '1' and tile.layout[j] == '0':
                    one += 1
                if tile.value[j] == '2' and tile.layout[j] == '0':
                    two += 1
                if tile.value[j] == '3' and tile.layout[j] == '0':
                    three += 1
                if tile.value[j] == '4' and tile.layout[j] == '0':
                    four += 1
        return [one, two, three, four]

    def final_check(self):
        """
        Checks if the current layout and color counts exactly meet the goal.
        Returns True if both currentLayoutCount equals layoutTarget and currentColorCount equals colorTarget.
        """
        for i in range(len(self.currentLayoutCount)):
            if self.currentLayoutCount[i] != self.layoutTarget[i]:
                return False
        for i in range(len(self.currentColorCount)):
            if self.currentColorCount[i] != self.colorTarget[i]:
                return False
        return True

    def layout_check(self):
        """
        Checks if layout numbers are within bounds and updates each Tile's domain if needed.
        If the current count for OUTER or EL equals the target, then for each tile, if the count
        exceeds the target and the tile's domain contains the corresponding symbol ('O' for OUTER,
        'E' for EL), the symbol is removed.
        Returns True if the layout is within bounds; otherwise, returns False.
        """
        # Create a copy of current layout counts.
        num_calc = self.currentLayoutCount.copy()
        if self.currentLayoutCount[0] == self.layoutTarget[0] or self.currentLayoutCount[1] == self.layoutTarget[1]:
            for tile in self.tiles:
                # For OUTER ("O")
                if num_calc[0] >= self.layoutTarget[0]:
                    if num_calc[0] > self.layoutTarget[0] and 'O' in tile.domain:
                        tile.domain.remove('O')
                    num_calc[0] += 1
                # For EL ("E")
                if num_calc[1] >= self.layoutTarget[1]:
                    if num_calc[1] > self.layoutTarget[1] and 'E' in tile.domain:
                        tile.domain.remove('E')
                    num_calc[1] += 1
        else:
            return self.currentLayoutCount[0] <= self.layoutTarget[0] and self.currentLayoutCount[1] <= self.layoutTarget[1]
        return True

    def target_check(self):
        """
        Checks if each bush color count is within its respective target.
        Returns True if for every color the current count is less than or equal to the target.
        """
        for i in range(len(self.currentColorCount)):
            if self.currentColorCount[i] > self.colorTarget[i]:
                return False
        return True

    def change_layout(self, tile_index, option, el):
        """
        Changes the layout of the tile at position tile_index.
          - option 0: assign OUTER layout.
          - option 1: assign EL layout using the specified el option (0 to 3).
          - option 2: assign FULL layout.
        After updating, the method recalculates counts, updates the distance metrics,
        and returns True if both layout and color checks pass.
        """
        if option == 0:
            self.tiles[tile_index].layout = Layouts.getOuter()
            self.tiles[tile_index].layoutName = "OUTER"
        elif option == 1:
            self.tiles[tile_index].layout = Layouts.getEl(el)
            self.tiles[tile_index].layoutName = f"EL {el}"
        elif option == 2:
            self.tiles[tile_index].layout = Layouts.getFull()
            self.tiles[tile_index].layoutName = "FULL"
        # Update counts and distances.
        self.currentLayoutCount = self.layout_number_calc()
        self.currentColorCount = self.target_number_calc()
        self.dist_calc()
        return self.layout_check() and self.target_check()

    def dist_calc(self):
        """
        Calculates the difference (distance) from current counts to the goal counts.
          - distLayout: sum of (target OUTER - current OUTER) and (target EL - current EL) 
                        plus (current FULL - target FULL).
          - distColor: sum of differences between target and current counts for bush colors.
        Lower values are considered better.
        """
        self.distLayout = ((self.layoutTarget[0] - self.currentLayoutCount[0]) +
                           (self.layoutTarget[1] - self.currentLayoutCount[1]) +
                           (self.currentLayoutCount[2] - self.layoutTarget[2]))
        self.distColor = ((self.colorTarget[0] - self.currentColorCount[0]) +
                          (self.colorTarget[1] - self.currentColorCount[1]) +
                          (self.colorTarget[2] - self.currentColorCount[2]) +
                          (self.colorTarget[3] - self.currentColorCount[3]))

    def tile_order(self):
        """
        Organizes tiles from the one with the fewest assigned bush values to the one with the most.
        For each tile, it counts the number of characters in tile.value that are in {'1','2','3','4'}.
        Returns a list of [tile_index, count] pairs sorted by count.
        """
        order = []
        for i, tile in enumerate(self.tiles):
            count = 0
            for char in tile.value:
                if char in {'1', '2', '3', '4'}:
                    count += 1
            order.append([i, count])
        order.sort(key=lambda pair: pair[1])
        return order

    def __eq__(self, other):
        """
        Checks equality between two Node objects.
        Two Nodes are equal if their layout and color counts are the same and all tile layouts match.
        """
        if not isinstance(other, Node):
            return False
        if self.currentLayoutCount != other.currentLayoutCount:
            return False
        if self.currentColorCount != other.currentColorCount:
            return False
        for tile1, tile2 in zip(self.tiles, other.tiles):
            if tile1.layout != tile2.layout:
                return False
        return True

    def __str__(self):
        """
        Returns a string representation of the Node.
        Displays each tile's information, current counts, goals, and distance metrics.
        """
        result = "Variable:\n"
        for i, tile in enumerate(self.tiles):
            result += f"\t | \t Tile: {i}\t | \t{tile}\n"
        result += "Tile Layout Count: " + str(self.layout_number_calc()) + "\n"
        result += "Tile Layout Goal: " + f"[OUTER {self.layoutTarget[0]}, EL {self.layoutTarget[1]}, FULL {self.layoutTarget[2]}]\n"
        result += "Target Number Count: " + str(self.target_number_calc()) + "\n"
        result += ("Target Number Goal: " +
                   f"[1: {self.colorTarget[0]}, 2: {self.colorTarget[1]}, 3: {self.colorTarget[2]}, 4: {self.colorTarget[3]}]\n")
        result += "Target Difference: " + str(self.distColor) + "\n"
        result += "Layout Difference: " + str(self.distLayout) + "\n"
        return result
