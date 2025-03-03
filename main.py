from FileReader import FileReader
from ConstraintProp import ConstraintProp
from SearchAlgorithm import csp_alg
import sys

def main():
    # Check if the input file argument is provided
    if len(sys.argv) < 2:
        print("Usage: python main.py <input_file>", file=sys.stderr)
        sys.exit(1)

    # Initialize FileReader and read the input file
    fr = FileReader()
    try:
        input_file = sys.argv[1]
        fr.read_file(input_file)
    except FileNotFoundError:
        print(f"File not found: {input_file}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

    # Process tiles and targets
    tiles = fr.get_tiles()             # 2D list (landscape as list of char lists)
    targets = fr.get_targets()          # List of target numbers for bush colors.
    tile_count = fr.get_tile_count()    # List of target counts for layouts.
    total_tiles = fr.get_total_tiles()  # Total number of tiles.

    # Run the CSP algorithm
    a = csp_alg(tiles, targets, tile_count, total_tiles)
    print(a)

if __name__ == '__main__':
    main()
