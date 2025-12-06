import numpy as np

def read_input(file_path):
    with open(file_path, 'r') as f:
        lines = [line.strip('\n') for line in f.readlines() if line.strip()]
    return lines

def parse_input_part_1(lines):
    numbers_array = np.zeros((len(lines)-1, len(lines[0].split())), dtype=int)
    do_multiply = []
    for i, line in enumerate(lines):
        l = line.split()
        if i < len(lines)-1:
            numbers_array[i, :] = l
        else:
            do_multiply = [1 if x == '*' else 0 for x in l]
    do_multiply = np.array(do_multiply, dtype=bool)
    do_add = ~do_multiply
    return numbers_array, do_multiply, do_add

def parse_input_part_2(lines):
    #get operations array
    operations = lines[-1].split()
    #find indices where all lines have a char of ' '
    space_indices = []
    space_indices.append(-1)
    # Find the maximum line length to know how many columns to check
    max_length = max(len(line) for line in lines)
    # For each column position, check if all lines have a space there
    for j in range(max_length):
        # Check if all lines have a space at position j
        if all(j < len(line) and line[j] == ' ' for line in lines):
            space_indices.append(j)
    space_indices.append(max_length)
    final_results = []
    for i in range(len(space_indices)-1):
        start_index = space_indices[i] + 1
        end_index = space_indices[i+1]
        # Get the operation for this segment
        op = operations[i]
        #create empty list with end_index-start_index elements
        numbers_list = [''] * (end_index - start_index)
        # For each column position in this segment
        for k in range(end_index - start_index):
            # Concatenate characters from all lines at this column position
            for j in range(len(lines)-1):
                char_index = start_index + k
                if char_index < len(lines[j]):
                    char = lines[j][char_index]
                    numbers_list[k] = numbers_list[k] + char
        # Strip strings and convert to numbers array (filter out empty strings)
        numbers_list = np.array([int(s.strip()) for s in numbers_list if s.strip()], dtype=int)
        # Apply operation immediately
        if op == '*':
            result = np.prod(numbers_list)
        elif op == '+':
            result = np.sum(numbers_list)
        final_results.append(result)
        print(f"Segment {i}: {op} of {numbers_list} = {result}")
    
    return np.array(final_results)


def calculate_result(numbers_array, do_multiply, do_add):
    result = np.zeros(len(numbers_array), dtype=int)
    add_array = do_add[None, :] * numbers_array
    multiply_array = do_multiply[None, :] * numbers_array
    result = np.sum(add_array, axis=0) + np.prod(multiply_array, axis=0)
    print(f"result: {result}")
    print(f"shape of result: {result.shape}")
    return result

lines = read_input('real_input.txt')
numbers_array, do_multiply, do_add = parse_input_part_1(lines)
print(f"numbers_array: {numbers_array}")
print(f"do_multiply: {do_multiply}")
print(f"do_add: {do_add}")
results_array = calculate_result(numbers_array, do_multiply, do_add)
print(f"results_array: {results_array}")

#Part 1: sum of results
print(f"sum of results: {np.sum(results_array)}")

#Part 2: parse input and calculate result
final_results = parse_input_part_2(lines)
print(f"final_results: {final_results}")
print(f"sum of final_results: {np.sum(final_results)}")
