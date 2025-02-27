import sys
from csp_solver import LandscapeCSPSolver
from utils import read_input
import time

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)
    N, landscape, tile_counts, targets = read_input(sys.argv[1])
    solver = LandscapeCSPSolver(N, landscape, tile_counts, targets)
    s = time.time()
    solver.solve()
    print("Time taken:", time.time() - s)