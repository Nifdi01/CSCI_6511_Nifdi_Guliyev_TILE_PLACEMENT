import unittest
from Tile import Tile
from Layouts import Layouts
from Node import Node
from Arc import Arc
from ConstraintProp import ConstraintProp
from Heuristic import Heuristic

##############################################
# Test for the Layouts class
##############################################
class TestLayouts(unittest.TestCase):
    def test_get_el_option0(self):
        # For EL option 0, expected indices: 0,1,2,3,4,8,12 should be '1', rest '0'
        expected_indices = {0, 1, 2, 3, 4, 8, 12}
        el0 = Layouts.getEl(0)
        self.assertEqual(len(el0), 16)
        for i in range(16):
            if i in expected_indices:
                self.assertEqual(el0[i], '1')
            else:
                self.assertEqual(el0[i], '0')
    
    def test_get_full(self):
        full = Layouts.getFull()
        self.assertEqual(len(full), 16)
        for c in full:
            self.assertEqual(c, '1')
    
    def test_get_outer(self):
        # Expected indices for OUTER: 0,1,2,3,4,7,8,11,12,13,14,15 are '1'
        expected_indices = {0, 1, 2, 3, 4, 7, 8, 11, 12, 13, 14, 15}
        outer = Layouts.getOuter()
        self.assertEqual(len(outer), 16)
        for i in range(16):
            if i in expected_indices:
                self.assertEqual(outer[i], '1')
            else:
                self.assertEqual(outer[i], '0')
    
    def test_get_initial_layout(self):
        initial = Layouts.getInitialLayout()
        self.assertEqual(initial, Layouts.getFull())

##############################################
# Test for the Tile class
##############################################
class TestTile(unittest.TestCase):
    def test_tile_str(self):
        value = ['1', '2', '3', '4'] * 4
        layout = ['0'] * 16
        name = "TEST"
        tile = Tile(value, layout, name)
        s = str(tile)
        self.assertIn("Value:", s)
        self.assertIn(name, s)

##############################################
# Dummy Node for testing Arc (since Arc uses node.target_number_calc())
##############################################
class DummyNode:
    def __init__(self, target):
        self._target = target
        self.parent = None
    def target_number_calc(self):
        return self._target
    def __eq__(self, other):
        return isinstance(other, DummyNode) and self._target == other._target

##############################################
# Test for the Arc class
##############################################
class TestArc(unittest.TestCase):
    def test_arc_methods(self):
        # Create two dummy nodes.
        n1 = DummyNode([1, 2, 3])
        n2 = DummyNode([4, 5, 3])
        n1.parent = None
        n2.parent = None
        arc1 = Arc(n1, n2)
        # For arc_create, we need to set n1.parent.
        n1.parent = n2
        arc2 = Arc.arc_create(n1)
        self.assertEqual(arc1.left(), n1)
        self.assertEqual(arc1.right(), n2)
        self.assertEqual(arc2.left(), n1)
        self.assertEqual(arc2.right(), n2)
        # Test string representation.
        s = str(arc1)
        self.assertIn("Arc Left:", s)
        self.assertIn("Arc Right:", s)
        # Test equality.
        self.assertEqual(arc1, arc2)

##############################################
# Test for the Node class
##############################################
class TestNode(unittest.TestCase):
    def setUp(self):
        # Create three sample tiles.
        self.tile_value = ['1', '2', '3', '4'] * 4
        # Use FULL layout initially.
        self.initial_layout = Layouts.getInitialLayout()
        self.tile1 = Tile(self.tile_value.copy(), self.initial_layout.copy(), "FULL")
        self.tile2 = Tile(self.tile_value.copy(), self.initial_layout.copy(), "FULL")
        self.tile3 = Tile(self.tile_value.copy(), self.initial_layout.copy(), "FULL")
        self.tiles = [self.tile1, self.tile2, self.tile3]
        # Set dummy targets:
        # For layouts: assume target is [1, 1, 1] (OUTER, EL, FULL)
        # For bush colors: target [4, 4, 4, 4]
        self.layout_target = [1, 1, 1]
        self.color_target = [4, 4, 4, 4]
        self.node = Node(self.tiles, self.color_target, self.layout_target)
    
    def test_layout_number_calc(self):
        # With all tiles as "FULL", expect 0 OUTER, 0 EL, and 3 FULL.
        calc = self.node.layout_number_calc()
        self.assertEqual(calc, [0, 0, 3])
    
    def test_target_number_calc(self):
        # Since layout is FULL (all ones) meaning bushes are covered,
        # uncovered counts should be zero.
        calc = self.node.target_number_calc()
        self.assertEqual(calc, [0, 0, 0, 0])
    
    def test_final_check(self):
        # With the current configuration, final_check should be False.
        self.assertFalse(self.node.final_check())
    
    def test_change_layout(self):
        # Change layout of tile 0 to OUTER (option 0) and verify the layout name updates.
        result = self.node.change_layout(0, option=0, el=0)
        self.assertTrue(result)
        self.assertEqual(self.node.tiles[0].layoutName, "OUTER")
    
    def test_tile_order(self):
        # Every tile’s value length is 16, so tile_order should return counts of 16.
        order = self.node.tile_order()
        for _, count in order:
            self.assertEqual(count, 16)

##############################################
# Test for ConstraintProp class
##############################################
class TestConstraintProp(unittest.TestCase):
    def test_arc_consistency(self):
        # Create a tile with an empty domain.
        value = ['1', '2', '3', '4'] * 4
        layout = ['0'] * 16
        tile = Tile(value.copy(), layout.copy(), "FULL")
        tile.domain = []  # clear the domain
        node = Node([tile], [4, 4, 4, 4], [1, 1, 1])
        # Initially, domain is empty.
        self.assertEqual(tile.domain, [])
        removed = ConstraintProp.arc_consistency(node)
        # After arc_consistency, domain should be restored.
        self.assertTrue(removed)
        self.assertEqual(tile.domain, ['O', 'E', 'F'])

##############################################
# Test for the Heuristic class
##############################################
class TestHeuristic(unittest.TestCase):
    def test_mrv_calc(self):
        # Create two nodes with different distColor values.
        node1 = Node([], [4, 4, 4, 4], [1, 1, 1])
        node2 = Node([], [4, 4, 4, 4], [1, 1, 1])
        node1.distColor = 10
        node2.distColor = 5
        open_list = [node1, node2]
        index = Heuristic.mrv_calc(open_list)
        # Expect node2 (with lower distColor) to be chosen.
        self.assertEqual(open_list[index], node2)
    
    def test_tie(self):
        # Create two nodes with equal distColor but different distLayout.
        node1 = Node([], [4, 4, 4, 4], [1, 1, 1])
        node2 = Node([], [4, 4, 4, 4], [1, 1, 1])
        node1.distColor = 10
        node2.distColor = 10
        node1.distLayout = 3
        node2.distLayout = 5
        open_list = [node1, node2]
        chosen = Heuristic.tie(0, 1, open_list)
        self.assertEqual(chosen, 1)
    
    def test_lcv_calc(self):
        # Create a Node with one tile whose domain includes 'E'.
        value = ['1', '2', '3', '4'] * 4
        layout = ['0'] * 16
        tile = Tile(value.copy(), layout.copy(), "FULL")
        tile.domain = ['E', 'O', 'F']
        node = Node([tile], [4, 4, 4, 4], [1, 1, 1])
        option = Heuristic.lcv_calc(node, 0)
        # Option should be one of the valid values: 0,1,2,3,4, or 5.
        self.assertIn(option, [0, 1, 2, 3, 4, 5])

##############################################
# Run all tests
##############################################
if __name__ == '__main__':
    unittest.main()
