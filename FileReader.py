import re

class FileReader:
    def __init__(self):
        # list of lines read from file (non-comments, non-empty)
        self.text = []
        # tile counts: order [OUTER_BOUNDARY, EL_SHAPE, FULL_BLOCK]
        self.tile_count = None
        # target values (for numbers 1 to 4)
        self.targets = None
        # list of tiles (each tile is a list of characters from a 4x4 block)
        self.tiles = None
        # total number of tiles computed as sum(tile_count)
        self.total_tiles = 0
        # 2D list representing the landscape (list of rows)
        self.landscape = None

    def read_file(self, filename):
        """Reads the input file and sets up landscape, tile counts, and targets."""
        # Open the file and read each line
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.rstrip('\n')
                # skip comment lines and empty lines
                if not line or line.strip().startswith("#"):
                    continue
                self.text.append(line)
        
        # Determine the dimension of the landscape: count lines until a line starting with '{'
        dimension = self.dimension_calc(self.text)
        
        # Parse tile counts from the tile info line (at index 'dimension')
        self.tile_count = self.set_tile_count(self.text[dimension])
        # Calculate total number of tiles (should match the sum of the tile counts)
        self.total_tiles = sum(self.tile_count)
        
        # Build the landscape (2D array) from the first 'dimension' lines
        self.landscape = self.build_landscape(self.text[:dimension])
        
        # Extract individual tiles from the landscape;
        # each tile is a 4x4 block and we stop when we have the expected total number of tiles.
        self.tiles = self.extract_tiles(self.landscape, tile_size=4, total_tiles=self.total_tiles)
        
        # Parse targets from the next 4 lines after the tile info line
        self.targets = self.set_targets(self.text[dimension + 1: dimension + 5])

    def dimension_calc(self, lines):
        """Returns the number of lines before the first line starting with '{'."""
        dimension = 0
        for line in lines:
            if line.strip().startswith('{'):
                break
            dimension += 1
        return dimension

    def set_tile_count(self, tile_line):
        """
        Parses the tile description line.
        Expected format: {EL_SHAPE=7, OUTER_BOUNDARY=10, FULL_BLOCK=8}
        Returns a list of three integers in the order:
            [OUTER_BOUNDARY, EL_SHAPE, FULL_BLOCK]
        """
        content = tile_line.strip('{}').strip()
        parts = content.split(',')
        tile_dict = {}
        for part in parts:
            part = part.strip()
            if '=' in part:
                key, value = part.split('=')
                tile_dict[key.strip()] = int(value.strip())
        outer = tile_dict.get("OUTER_BOUNDARY", 0)
        el = tile_dict.get("EL_SHAPE", 0)
        full = tile_dict.get("FULL_BLOCK", 0)
        return [outer, el, full]

    def build_landscape(self, lines):
        """
        Constructs the landscape as a 2D list (list of rows), where each row
        is built by taking every other character from the input line.
        Uses the length of the first line as a baseline and pads shorter lines.
        """
        landscape = []
        # Use the first line's length as baseline.
        base_length = len(lines[0])
        for line in lines:
            # Pad line with spaces if it is shorter than the first line.
            if len(line) < base_length:
                line = line.ljust(base_length)
            # Take characters at even indices (0, 2, 4, ...) up to base_length.
            row = [line[i] for i in range(0, base_length, 2)]
            landscape.append(row)
        return landscape

    def extract_tiles(self, landscape, tile_size=4, total_tiles=0):
        """
        Divides the landscape into non-overlapping 4x4 blocks.
        Assumes the landscape is a square of size 'dimension'.
        Returns a list of tiles, where each tile is a list of characters.
        """
        tiles = []
        # Calculate number of tiles per row and column based on landscape rows (each row is now uniform)
        n_tiles_row = len(landscape) // tile_size
        n_tiles_col = len(landscape[0]) // tile_size
        
        for tile_row in range(n_tiles_row):
            for tile_col in range(n_tiles_col):
                if len(tiles) >= total_tiles:
                    break  # stop if we reached the expected number of tiles
                tile_chars = []
                for r in range(tile_row * tile_size, (tile_row + 1) * tile_size):
                    for c in range(tile_col * tile_size, (tile_col + 1) * tile_size):
                        tile_chars.append(landscape[r][c])
                tiles.append(tile_chars)
            if len(tiles) >= total_tiles:
                break
        return tiles

    def set_targets(self, target_lines):
        """
        Parses target lines.
        Each target line is expected in the format: "X:Y" (e.g., "1:24").
        Returns a list of target numbers [24, 21, 18, 17].
        """
        targets = []
        for line in target_lines:
            if ':' in line:
                _, value = line.split(':')
                targets.append(int(value.strip()))
        return targets

    # Getter methods
    def get_targets(self):
        return self.targets

    def get_tiles(self):
        return self.tiles

    def get_tile_count(self):
        return self.tile_count

    def get_total_tiles(self):
        return self.total_tiles
