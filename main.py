import sys
from csp_solver import solve_csp
from utils import read_input
import time

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <input_file>")
        sys.exit(1)
    N, landscape, tile_counts, targets = read_input(sys.argv[1])
    s = time.time()
    solve_csp(N, landscape, tile_counts, targets)
    print("Time taken:", time.time() - s)