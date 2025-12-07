def read_input(file_path):
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    return lines

def part1_2(lines):
    current_indices = [lines[0].index('S')]
    num_splits = 0
    number_paths = 1
    beams_at_index= [0] * len(lines)
    beams_at_index[lines[0].index('S')] = 1
    for i in range(1, len(lines)):
        line = lines[i]
        #get where all ^ are
        hat_indices = [j for j, char in enumerate(line) if char == '^']
        #check if any of the hat indices are in the current indices
        for j in range(len(current_indices)):
            current_index = current_indices[j]
            if current_index in hat_indices:
                num_splits += 1
                number_paths += beams_at_index[current_index]
                current_indices[j] = current_index - 1
                current_indices.append(current_index + 1)
                beams_at_index[current_index - 1] += beams_at_index[current_index]
                beams_at_index[current_index + 1] += beams_at_index[current_index]
                beams_at_index[current_index] = 0
        #remove duplicates from current indices
        current_indices = list(set(current_indices))
    return num_splits, number_paths

lines = read_input('real_input.txt')
num_splits, number_paths = part1_2(lines)
print(f"num of splits: {num_splits}")
print(f"number of paths: {number_paths}")