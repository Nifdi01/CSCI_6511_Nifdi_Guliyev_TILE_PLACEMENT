from Arc import Arc

class ConstraintProp:
    @staticmethod
    def AC3(neighbors):
        """
        Enforces arc consistency on an initial grid.
        neighbors: list of Node objects.
        Returns True if arc consistency holds, otherwise False.
        """
        # Create a list of arcs from each neighbor using Arc.arc_create
        arcs = []
        nei = neighbors  # original neighbor list
        for neighbor in neighbors:
            arc = Arc.arc_create(neighbor)
            arcs.append(arc)
            
        # Process arcs until none remain.
        while arcs:
            # Get the first arc (removing it from the list)
            arc = arcs.pop(0)
            n = arc.left()  # the left node of the arc
            # If enforcing arc consistency on the left node causes changes...
            if ConstraintProp.arc_consistency(arc.left()):
                # If the layout distance is nonpositive, the grid is inconsistent.
                if arc.left().distLayout <= 0:
                    return False
                # Otherwise, add arcs for all other nodes (neighbors) except n.
                for next_node in nei:
                    if next_node != n:
                        new_arc = Arc.arc_create(next_node)
                        arcs.append(new_arc)
        return True

    @staticmethod
    def arc_consistency(node):
        """
        Checks if the node's current layout and color counts are outside target bounds.
        For layout counts, it iterates over indices except the last one (assumed to be FULL)
        and also verifies that the FULL count is not below target.
        For color counts, it verifies that each count does not exceed its target.
        Additionally, if any tile's domain is empty, it repopulates it with ['O', 'E', 'F'].
        Returns True if any inconsistency (or domain removal) is detected.
        """
        removed = False
        # Check layout counts for indices 0 to length-2 (excluding FULL) 
        for i in range(len(node.currentLayoutCount) - 1):
            if node.currentLayoutCount[i] > node.layoutTarget[i]:
                removed = True
                break
        # Check FULL count (assumed to be at index 2)
        if node.currentLayoutCount[2] < node.layoutTarget[2]:
            removed = True
        # Check color counts for each bush type
        for i in range(len(node.currentColorCount)):
            if node.currentColorCount[i] > node.colorTarget[i]:
                removed = True
                break
        # If any tile's domain is empty, restore the default domain values.
        for tile in node.tiles:
            if not tile.domain:  # domain is empty
                removed = True
                tile.domain.extend(['O', 'E', 'F'])
        return removed
