def parse_landscape_line(line, cell_width=2):
    """
    Process a fixed-width line representing a grid row.
    
    Each row is exactly (num_cols * cell_width) characters long.
    A cell with a number will have its digit (and possibly a trailing space).
    A missing cell is represented by two spaces.
    
    This function slices the line into chunks of cell_width,
    strips each chunk, and converts nonempty chunks to int.
    Empty cells become 0.
    """
    # If the line isn’t a multiple of cell_width, pad it to the right.
    if len(line) % cell_width != 0:
        line = line.ljust(((len(line) // cell_width) + 1) * cell_width)
    
    tokens = []
    for i in range(0, len(line), cell_width):
        cell = line[i:i+cell_width]
        token = cell.strip()
        if token == '':
            tokens.append(0)
        else:
            tokens.append(int(token))
    return tokens

def read_input(filename):
    with open(filename, 'r') as f:
        # Read lines while keeping trailing spaces.
        # Also ignore empty lines.
        lines = [line.rstrip('\n') for line in f if line.strip()]
    
    # Find indices for sections (if using a file with sections)
    landscape_start = next((i for i, line in enumerate(lines) if line.startswith('# Landscape')), 0)
    tiles_index = next((i for i, line in enumerate(lines) if line.startswith('# Tiles:')), -1)
    targets_index = next((i for i, line in enumerate(lines) if line.startswith('# Targets:')), -1)
    
    if tiles_index == -1 or targets_index == -1:
        raise ValueError("Input file missing required sections: # Tiles: or # Targets:")
    
    # --- Parse Landscape ---
    # The landscape lines are those between the '# Landscape' header and '# Tiles:'
    landscape_lines = lines[landscape_start + 1:tiles_index]
    landscape = []
    
    for line in landscape_lines:
        row = parse_landscape_line(line)
        # print(row)  # debug print to see each parsed row
        landscape.append(row)
    
    # Determine the expected number of columns as the max row length.
    num_cols = max(len(row) for row in landscape)
    # Pad (or truncate) each row so that every row has exactly num_cols tokens.
    for row in landscape:
        if len(row) < num_cols:
            row.extend([0] * (num_cols - len(row)))
        elif len(row) > num_cols:
            del row[num_cols:]
    
    num_rows = len(landscape)
    # Validate that the grid is square and its dimensions are divisible by 4.
    if num_rows != num_cols or num_rows % 4 != 0:
        raise ValueError("Landscape must be a square grid with dimensions divisible by 4")
    
    N = num_rows  # grid dimension
    
    # --- Parse Tile Counts ---
    tiles_line = lines[tiles_index + 1].strip('{}')
    tile_counts = {}
    try:
        for pair in tiles_line.split(','):
            key, value = pair.split('=')
            tile_counts[key.strip()] = int(value.strip())
    except Exception as e:
        raise ValueError(f"Error parsing tile counts: {tiles_line}. Exception: {e}")
    
    # --- Parse Targets ---
    targets = {}
    for line in lines[targets_index + 1:]:
        if line.startswith('#'):
            break
        color, count = map(int, line.split(':'))
        targets[color] = count
    
    return N, landscape, tile_counts, targets


def get_neighbors(var, variables):
    i, j = var
    k = int(len(variables) ** 0.5)
    neighbors = []
    if i > 0:
        neighbors.append((i-1, j))  # up
    if j > 0:
        neighbors.append((i, j-1))  # left
    if i < k - 1:
        neighbors.append((i+1, j))  # down
    if j < k - 1:
        neighbors.append((i, j+1))  # right
    return [n for n in neighbors if n in variables]