import numpy as np

def read_input(file_path):
    all_strings = []
    with open(file_path, 'r') as f:
        for line in f.readlines():
            all_strings.append(line.strip('\n'))
    return all_strings

def find_largest_number(input_string, output_length):
    start_index = 0
    largest_string = ''
    for i in range(output_length-1, -1, -1):
        end_index = None if i == 0 else -i
        slice_str = input_string[start_index:end_index]
        relative_pos, largest_number = max(enumerate(slice_str), key=lambda x: x[1])
        largest_number_position = start_index + relative_pos
        largest_string += largest_number
        start_index = largest_number_position + 1
    return int(largest_string)

input_strings = read_input('real_input.txt')
num_batteries = 12
largest_numbers = []
for input_string in input_strings:
    largest_numbers.append(find_largest_number(input_string, num_batteries))
print(f"largest_numbers: {largest_numbers}")
sum_largest_numbers = np.sum(largest_numbers)
print(f"sum_largest_numbers: {sum_largest_numbers}")
