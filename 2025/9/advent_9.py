import numpy as np

def read_input(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    return lines

def input_to_coords(lines):
    x_coords = []
    y_coords = []
    for line in lines:
        x, y = line.split(',')
        x_coords.append(int(x))
        y_coords.append(int(y))
    return np.column_stack([x_coords, y_coords])

def compute_square_sizes(coords):
    diff = coords[:, None, :] - coords[None, :, :]
    # Compute (abs(x1-x2)+1) * (abs(y1-y2)+1) for all pairs
    square_sizes = (np.abs(diff[:, :, 0]) + 1) * (np.abs(diff[:, :, 1]) + 1)
    return square_sizes

def find_largest_square(square_sizes, coords):
    max_size = np.max(square_sizes)
    # Find indices where maximum occurs (returns first occurrence)
    max_indices = np.unravel_index(np.argmax(square_sizes), square_sizes.shape)
    i, j = max_indices
    coord_pair = np.array([coords[i], coords[j]])
    return max_size, coord_pair

#part 1
lines = read_input('example_input.txt')
coords = input_to_coords(lines)
square_sizes = compute_square_sizes(coords)
max_size, coord_pair = find_largest_square(square_sizes, coords)
print(f"Largest square size: {max_size}")
print(f"Coordinates of the two points: {coord_pair}")


#part 2
def make_green_tiles_border(coords):
    green_tiles = []
    n = len(coords)
    
    for i in range(n):
        # Get current and next coordinate (wrapping around)
        p1 = coords[i]
        p2 = coords[(i + 1) % n]
        
        # Calculate direction vector
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        
        # Number of steps (excluding endpoints)
        num_steps = max(abs(dx), abs(dy)) - 1
        
        if num_steps > 0:
            # Calculate step direction (normalize to unit steps)
            step_x = np.sign(dx) if dx != 0 else 0
            step_y = np.sign(dy) if dy != 0 else 0
            
            # Generate step indices: 1, 2, ..., num_steps
            steps = np.arange(1, num_steps + 1)
            
            # Vectorized coordinate generation
            x_coords = p1[0] + steps * step_x
            y_coords = p1[1] + steps * step_y
            
            # Stack into (num_steps, 2) array
            segment_tiles = np.column_stack([x_coords, y_coords])
            green_tiles.append(segment_tiles)
    
    # Concatenate all segments at once
    return np.vstack(green_tiles)

def is_valid_square(coords, border_tiles):
    n = len(coords)
    valid = np.zeros((n, n), dtype=bool)
    
    # Sort by y, then by x for efficient grouping
    sort_indices = np.lexsort((border_tiles[:, 0], border_tiles[:, 1]))
    sorted_tiles = border_tiles[sort_indices]
    
    # Find unique y values and their start indices
    unique_ys, y_indices = np.unique(sorted_tiles[:, 1], return_index=True)
    
    # Compute min/max x for each y group
    y_to_x_range = {}
    for i in range(len(unique_ys)):
        y = unique_ys[i]
        start_idx = y_indices[i]
        end_idx = y_indices[i + 1] if i + 1 < len(y_indices) else len(sorted_tiles)
        
        # Get x coordinates for this y (already sorted)
        x_coords_at_y = sorted_tiles[start_idx:end_idx, 0]
        y_to_x_range[y] = (x_coords_at_y[0], x_coords_at_y[-1])  # min and max (already sorted)
    
    # Convert y_to_x_range to arrays
    all_ys = np.array(list(y_to_x_range.keys()))
    y_min = np.min(all_ys)
    y_max = np.max(all_ys)
    
    # Create lookup arrays: for any y, get min_x and max_x
    # Use a sparse approach: only store values for y that exist
    y_exists = np.zeros(y_max - y_min + 1, dtype=bool)
    y_min_x_lookup = np.zeros(y_max - y_min + 1, dtype=int)
    y_max_x_lookup = np.zeros(y_max - y_min + 1, dtype=int)
    
    for y, (min_x, max_x) in y_to_x_range.items():
        idx = y - y_min
        y_exists[idx] = True
        y_min_x_lookup[idx] = min_x
        y_max_x_lookup[idx] = max_x
    
    # Vectorize rectangle bounds computation
    p1 = coords[:, None, :]  # (n, 1, 2)
    p2 = coords[None, :, :]   # (1, n, 2)
    
    min_xs = np.minimum(p1[:, :, 0], p2[:, :, 0])  # (n, n)
    max_xs = np.maximum(p1[:, :, 0], p2[:, :, 0])  # (n, n)
    min_ys = np.minimum(p1[:, :, 1], p2[:, :, 1])  # (n, n)
    max_ys = np.maximum(p1[:, :, 1], p2[:, :, 1])  # (n, n)
    
    # Vectorized checking: for each rectangle, check all rows at once
    for i in range(n):
        for j in range(n):
            rect_min_x = min_xs[i, j]
            rect_max_x = max_xs[i, j]
            rect_min_y = min_ys[i, j]
            rect_max_y = max_ys[i, j]
            
            # Check if rectangle y range is within valid y range
            if rect_min_y < y_min or rect_max_y > y_max:
                valid[i, j] = False
                continue
            
            # Get indices for y range
            y_start_idx = rect_min_y - y_min
            y_end_idx = rect_max_y - y_min + 1
            
            # Check if all y values in rectangle exist
            y_range_exists = y_exists[y_start_idx:y_end_idx]
            if not np.all(y_range_exists):
                valid[i, j] = False
                continue
            
            # Check if rectangle x range fits within all y ranges
            y_range_min_x = y_min_x_lookup[y_start_idx:y_end_idx]
            y_range_max_x = y_max_x_lookup[y_start_idx:y_end_idx]
            
            # Rectangle is valid if rect_min_x >= all y_min_x and rect_max_x <= all y_max_x
            if np.all(rect_min_x >= y_range_min_x) and np.all(rect_max_x <= y_range_max_x):
                valid[i, j] = True
            else:
                valid[i, j] = False
    
    return valid

def find_max_valid_square_size(coords, border_tiles):
    print("checking if squares are valid 1")
    valid = is_valid_square(coords, border_tiles)
    print("computing square sizes")
    square_sizes = compute_square_sizes(coords)
    print("finding maximum valid square size")
    
    # Only consider valid squares
    valid_square_sizes = np.where(valid, square_sizes, 0)
    
    max_size = np.max(valid_square_sizes)
    max_indices = np.unravel_index(np.argmax(valid_square_sizes), valid_square_sizes.shape)
    i, j = max_indices
    coord_pair = np.array([coords[i], coords[j]])
    
    return max_size, coord_pair

red_tiles = coords
print("getting green tiles border")
green_tiles_border = make_green_tiles_border(coords)
print("concatenating red and green tiles")
border_tiles = np.concatenate([red_tiles, green_tiles_border])
max_size, coord_pair = find_max_valid_square_size(coords, border_tiles)
print(f"Maximum valid square size: {max_size}")
print(f"Coordinates of the two points: {coord_pair}")

