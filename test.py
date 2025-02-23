import unittest
import os
import io
from contextlib import redirect_stdout
from csp_solver import solve_csp
from utils import read_input

class TestCSPSolver(unittest.TestCase):
    
    def setUp(self):
        # Define the folder containing input files
        self.input_dir = "inputs"
        if not os.path.exists(self.input_dir):
            os.makedirs(self.input_dir)  # Create folder if it doesn't exist (for CI/testing)
            self.skipTest(f"Input directory '{self.input_dir}' created but empty; populate with test files")
    
    def test_input_file_parsing_and_solution(self):
        # Check if the inputs folder has any .txt files
        input_files = [f for f in os.listdir(self.input_dir) if f.endswith(".txt")]
        if not input_files:
            self.skipTest(f"No .txt files found in '{self.input_dir}'")
        
        # Test each input file
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
                self.assertTrue(all(len(row) == N for row in landscape), f"{filename}: Inconsistent row lengths")
                self.assertEqual(N % 4, 0, f"{filename}: N must be a multiple of 4")
                expected_tile_count = (N // 4) ** 2
                self.assertEqual(sum(tile_counts.values()), expected_tile_count,
                               f"{filename}: Tile count {sum(tile_counts.values())} does not match expected {expected_tile_count}")
                self.assertTrue(all(k in ['FULL_BLOCK', 'OUTER_BOUNDARY', 'EL_SHAPE'] for k in tile_counts),
                              f"{filename}: Invalid tile types")
                self.assertTrue(all(isinstance(t, int) and t >= 0 for t in targets.values()),
                              f"{filename}: Targets must be non-negative integers")
                
                # Run the solver and capture output
                f = io.StringIO()
                with redirect_stdout(f):
                    solve_csp(N, landscape, tile_counts, targets)
                output = f.getvalue()
                
                # Verify solver output
                self.assertTrue("Solution found" in output or "No solution found" in output,
                              f"{filename}: Solver did not terminate correctly")
                
                if "Solution found" in output:
                    # Parse the output to check tile assignments and uncovered counts
                    lines = output.splitlines()
                    tile_assignments = []
                    uncovered_section = False
                    uncovered_counts = {}
                    
                    for line in lines:
                        if "Solution found" in line:
                            continue
                        elif "Uncovered Counts" in line:
                            uncovered_section = True
                            continue
                        elif uncovered_section and line.strip():
                            color, count = map(int, line.split(':'))
                            uncovered_counts[color] = count
                        elif line.strip() and not uncovered_section:
                            parts = line.split()
                            self.assertEqual(len(parts), 3, f"{filename}: Invalid assignment line: {line}")
                            idx, size, tile_type = int(parts[0]), int(parts[1]), parts[2]
                            self.assertEqual(size, 4, f"{filename}: Tile size must be 4")
                            self.assertIn(tile_type, ['FULL_BLOCK', 'OUTER_BOUNDARY', 'EL_SHAPE'],
                                        f"{filename}: Invalid tile type {tile_type}")
                            tile_assignments.append(tile_type)
                    
                    # Verify number of tiles matches expected
                    self.assertEqual(len(tile_assignments), expected_tile_count,
                                   f"{filename}: Number of tiles assigned ({len(tile_assignments)}) does not match {expected_tile_count}")
                    
                    # Verify tile counts match input
                    assigned_counts = {'FULL_BLOCK': 0, 'OUTER_BOUNDARY': 0, 'EL_SHAPE': 0}
                    for tile in tile_assignments:
                        assigned_counts[tile] += 1
                    for tile_type in tile_counts:
                        self.assertEqual(assigned_counts[tile_type], tile_counts[tile_type],
                                       f"{filename}: Assigned {tile_type} count ({assigned_counts[tile_type]}) does not match input ({tile_counts[tile_type]})")
                    
                    # Verify uncovered counts match targets
                    for color, target_count in targets.items():
                        self.assertIn(color, uncovered_counts,
                                    f"{filename}: Color {color} missing in uncovered counts")
                        self.assertEqual(uncovered_counts[color], target_count,
                                       f"{filename}: Uncovered count for color {color} ({uncovered_counts[color]}) does not match target ({target_count})")
                    for color in uncovered_counts:
                        self.assertIn(color, targets,
                                    f"{filename}: Unexpected color {color} in uncovered counts")

    def test_invalid_file_format(self):
        # Test a malformed input file
        invalid_input = """
        # Landscape
        1 2 3
        4 5  # Inconsistent row length
        # Tiles
        {FULL_BLOCK=1}
        # Targets
        1:1
        """
        temp_file = os.path.join(self.input_dir, "temp_invalid.txt")
        with open(temp_file, 'w') as f:
            f.write(invalid_input)
        
        N, landscape, tile_counts, targets = read_input(temp_file)
        self.assertEqual(N, 2)  # Should parse first row length
        self.assertEqual(len(landscape), 2)
        self.assertNotEqual(len(landscape[0]), len(landscape[1]))  # Inconsistent rows
        
        # Clean up
        os.remove(temp_file)

if __name__ == '__main__':
    unittest.main()