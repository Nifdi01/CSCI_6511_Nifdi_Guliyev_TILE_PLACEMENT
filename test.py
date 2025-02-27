import unittest
import os
import io
from contextlib import redirect_stdout
from csp_solver import LandscapeCSPSolver
from utils import read_input
from ac3 import AC3ConstraintPropagator

class TestCSPSolver(unittest.TestCase):
    
    def setUp(self):
        self.input_dir = "inputs"
        if not os.path.exists(self.input_dir):
            os.makedirs(self.input_dir)
            self.skipTest(f"Input directory '{self.input_dir}' created but empty; populate with test files")
    
    def test_input_file_parsing_and_solution(self):
        input_files = [f for f in os.listdir(self.input_dir) if f.endswith(".txt")]
        if not input_files:
            self.skipTest(f"No .txt files found in '{self.input_dir}'")
        
        for filename in input_files:
            with self.subTest(filename=filename):
                filepath = os.path.join(self.input_dir, filename)
                
                # Parse the input file
                try:
                    N, landscape, tile_counts, targets = read_input(filepath)
                except Exception as e:
                    self.fail(f"Failed to parse {filename}: {str(e)}")
                
                # Verify parsed input
                self.assertEqual(N, len(landscape), f"{filename}: Landscape size mismatch")
                self.assertTrue(all(len(row) == N for row in landscape), 
                              f"{filename}: Inconsistent row lengths")
                self.assertEqual(N % 4, 0, f"{filename}: N must be a multiple of 4")
                expected_tile_count = (N // 4) ** 2
                self.assertEqual(sum(tile_counts.values()), expected_tile_count,
                               f"{filename}: Invalid total tile count")
                
                # Create and run solver
                solver = LandscapeCSPSolver(N, landscape, tile_counts, targets)
                f = io.StringIO()
                with redirect_stdout(f):
                    result = solver.solve()
                output = f.getvalue()
                
                # Verify solver behavior
                if result:
                    self.verify_solution(solver, N, tile_counts, targets, filename)
                else:
                    self.assertIn("No solution found", output, 
                                f"{filename}: Solver failed without proper message")
    
    def verify_solution(self, solver, N, tile_counts, targets, filename):
        """Verify the correctness of the found solution"""
        # Verify tile assignments
        assigned_counts = {}
        
        # Initialize count for each tile type
        for tile_type in tile_counts.keys():
            assigned_counts[tile_type] = 0
        
        # Map tile type indices to names based on the constants
        tile_type_map = {0: 'FULL_BLOCK', 1: 'OUTER_BOUNDARY', 2: 'EL_SHAPE'}
        
        # Count assigned tiles by type
        for var, val in solver.assignment.items():
            self.assertIsNotNone(val, f"{filename}: Incomplete assignment")
            tile_type = tile_type_map[val]
            assigned_counts[tile_type] += 1
        
        # Verify tile counts match input
        for tile_type, count in tile_counts.items():
            self.assertEqual(assigned_counts[tile_type], count,
                           f"{filename}: Incorrect {tile_type} count. Got {assigned_counts[tile_type]}, expected {count}")
        
        # Verify visibility requirements
        visible = solver.get_visible(solver.assignment)
        for color, target in targets.items():
            self.assertEqual(visible[color-1], target,
                           f"{filename}: Visibility requirement not met for color {color}")
    
    def test_constraint_propagation(self):
        """Test AC-3 constraint propagation"""
        N = 4  # Minimal valid grid size
        landscape = [[1, 2, 3, 4] * (N//4)] * N
        tile_counts = {'FULL_BLOCK': 1, 'OUTER_BOUNDARY': 0, 'EL_SHAPE': 0}
        targets = {1: 0, 2: 0, 3: 0, 4: 0}
        
        solver = LandscapeCSPSolver(N, landscape, tile_counts, targets)
        # Test that AC-3 maintains arc consistency
        ac3 = AC3ConstraintPropagator(solver.variables)
        self.assertTrue(ac3.propagate(None, None, solver.domains, {}))
    
    def test_invalid_inputs(self):
        """Test handling of invalid inputs"""
        test_cases = [
            # Non-square grid
            ([[1, 2], [1]], {'FULL_BLOCK': 1}, {1: 0}),
            # Invalid tile counts
            ([[1, 2], [1, 2]], {'INVALID_TILE': 1}, {1: 0}),
            # Invalid target colors
            ([[1, 2], [1, 2]], {'FULL_BLOCK': 1}, {5: 0})
        ]
        
        for landscape, tile_counts, targets in test_cases:
            with self.assertRaises(ValueError):
                LandscapeCSPSolver(len(landscape), landscape, tile_counts, targets)

if __name__ == '__main__':
    unittest.main()