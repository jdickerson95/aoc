import numpy as np


def parse_input(file_path):
    ranges = []
    tests = []
    with open(file_path, 'r') as f:
        do_ranges = True
        for line in f.readlines():
            l = line.strip()
            if l == '':
                do_ranges = False
                continue
            if do_ranges:
                ranges.append(l)
            else:
                tests.append(int(l))
    return ranges, np.array(tests, dtype=int)

def convert_ranges_to_array(ranges):
    array = np.zeros((len(ranges), 2),dtype=int)
    for i, r in enumerate(ranges):
        l = r.split('-')
        array[i, 0] = int(l[0]) # min
        array[i, 1] = int(l[1]) # max
    return array

def evaluate_tests(tests_array, ranges_array):
    # Check if each test falls within any range
    # Shape: (num_tests, num_ranges)
    in_range = (tests_array[:, None] >= ranges_array[:, 0]) & (tests_array[:, None] <= ranges_array[:, 1])
    # Check if each test falls within at least one range
    return np.any(in_range, axis=1)

def sort_ranges(ranges_array):
    # sort ranges_array by min
    return ranges_array[ranges_array[:, 0].argsort()]

def remove_overlap(ranges_array):
    # Build a new array with merged ranges
    merged = [ranges_array[0].copy()]
    for i in range(1, len(ranges_array)):
        current = ranges_array[i]
        last_merged = merged[-1]
        # If current range overlaps or is adjacent to last merged range
        if current[0] <= last_merged[1]:
            # Merge: extend the last merged range if needed
            last_merged[1] = max(last_merged[1], current[1])
        else:
            # No overlap, add as new range
            merged.append(current.copy())
    return np.array(merged)

# part 1 - get number of fresh in test set
ranges, tests = parse_input('real_input.txt')
ranges_array = convert_ranges_to_array(ranges)
#print(f"fresh_list: {fresh_list}")
print(f"tests: {tests}")
is_fresh = evaluate_tests(tests, ranges_array)
for i, test in enumerate(tests):
    if is_fresh[i]:
        print(f"test {test} is fresh")
    else:
        print(f"test {test} is spoiled")
print(f"count of fresh: {np.sum(is_fresh)}")

# part 2, get total number possible fresh in all ranges
# this must account for overlap

ranges_array = sort_ranges(ranges_array)
print(f"sorted ranges: {ranges_array}")
ranges_array = remove_overlap(ranges_array)
print(f"removed overlap ranges: {ranges_array}")
total_possible_fresh = np.sum(ranges_array[:, 1] - ranges_array[:, 0] + 1)
print(f"total possible fresh: {total_possible_fresh}")