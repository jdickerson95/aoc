import numpy as np
from scipy.ndimage import convolve

def read_input(file_path):
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    # Convert '@' to 1 and '.' to 0
    arr = np.array([[1 if char == '@' else 0 for char in line] for line in lines])
    return arr

def part1(arr, kernel, fewer_than):
    neighbor_sums = convolve(arr, kernel, mode='constant', cval=0)

    print("\nSum of 8 neighbors for each position:")
    print(neighbor_sums)

    # Count '@' symbols (arr == 1) that have fewer than 4 neighbors (neighbor_sums < 4)
    count = np.count_nonzero((arr == 1) & (neighbor_sums < fewer_than))
    print(f"Count of @ symbols with fewer than {fewer_than} neighbors: {count}")
    return count

def remove_possible_ones(arr, kernel, fewer_than):
    can_remove = True
    rolling_sum = 0
    current_arr = arr.copy()
    while can_remove:
        #convolve the current array with the kernel to get the neighbor sums
        neighbor_sums = convolve(current_arr, kernel, mode='constant', cval=0)
        remove_arr = np.where((neighbor_sums < fewer_than) & (current_arr == 1), 1, 0)
        sum_removed = np.sum(remove_arr)
        if sum_removed == 0:
            can_remove = False
            break
        rolling_sum += np.sum(remove_arr)
        current_arr = np.where(remove_arr == 1, 0, current_arr)

    return rolling_sum

# Read example input into 2D numpy array
arr = read_input('real_input.txt')
print("Original Array:")
print(arr)

# Define a 3x3 kernel for summing all 8 neighbors
# The center (1, 1) is 0 to exclude the current cell
kernel = np.array([[1, 1, 1],
                   [1, 0, 1],
                   [1, 1, 1]])

fewer_than = 4
part1(arr, kernel, fewer_than)

rolling_sum = remove_possible_ones(arr, kernel, fewer_than)
print(f"Rolling sum: {rolling_sum}")

