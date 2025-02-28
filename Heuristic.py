class Heuristic:
    @staticmethod
    def mrv_calc(open_list):
        """
        Minimum Remaining Values (MRV) heuristic.
        Returns the index of the node in open_list with the smallest distColor.
        In case of ties, the tie method is used (based on distLayout).
        """
        index = 0
        min_val = float('inf')
        for i, node in enumerate(open_list):
            # Check if the current node's color distance is smaller than the minimum found so far.
            if node.distColor < min_val:
                min_val = node.distColor
                index = i
            # If equal, use the tie breaker (degree heuristic based on distLayout).
            if node.distColor == min_val:
                min_i = Heuristic.tie(i, index, open_list)
                if min_i != index:
                    index = min_i
                    min_val = node.distColor
        return index

    @staticmethod
    def lcv_calc(neighbor, index):
        """
        Least Constraining Value (LCV) heuristic.
        For the tile at neighbor.tiles[index], consider layout options.
        For EL layouts, try options 0-3 if 'E' is in the tile's domain.
        For the OUTER layout, try option 4 if 'O' is in the domain.
        Returns the layout option (0-4) that results in the highest distColor.
        """
        dist_temp = -float('inf')
        layout_option = 5  # default value if no option is valid
        for j in range(6):
            # For EL layouts (options 0-3)
            if j < 4 and 'E' in neighbor.tiles[index].domain:
                if neighbor.change_layout(index, option=1, el=j):
                    if neighbor.distColor > dist_temp:
                        dist_temp = neighbor.distColor
                        layout_option = j
            # For the OUTER layout (option 4)
            elif j == 4 and 'O' in neighbor.tiles[index].domain:
                if neighbor.change_layout(index, option=0, el=0):
                    if neighbor.distColor > dist_temp:
                        dist_temp = neighbor.distColor
                        layout_option = j
        return layout_option

    @staticmethod
    def tie(current_index, current_min, open_list):
        """
        Tie breaker: if two nodes have the same distColor, 
        return the index of the node with the greater distLayout.
        """
        current = open_list[current_index]
        min_node = open_list[current_min]
        if current.distLayout > min_node.distLayout:
            return current_index
        else:
            return current_min