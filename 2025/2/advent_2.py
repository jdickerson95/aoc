import numpy as np

def read_input(file_path):
    all_ids = []
    with open(file_path, 'r') as f:
        for line in f.readlines():
            l = line.strip().split(',')
            for string in l:
                id_start, id_end = string.split('-')
                all_ids.append(np.arange(int(id_start), int(id_end) + 1))
    all_ids = np.concatenate(all_ids)
    return all_ids

def get_invalid_ids_rule_1(all_ids):
    # invalid is a sequence of numbers that repeats exactly twice
    # must be even length
    invalid_ids = []
    for i in range(len(all_ids)):
        if len(str(all_ids[i])) % 2 == 0: # even length
            #split into two halves
            half_length = len(str(all_ids[i])) // 2
            first_half = str(all_ids[i])[:half_length]
            second_half = str(all_ids[i])[half_length:]
            if first_half == second_half:
                invalid_ids.append(all_ids[i])
    
    np.array(invalid_ids)
    return invalid_ids

def get_factors_dict(all_ids):
    # Get all unique lengths of numbers in the list
    lengths = set()
    for num in all_ids:
        lengths.add(len(str(num)))
    
    # Create dictionary with length as key and factors as values
    factors_dict = {}
    for length in lengths:
        factors = []
        for i in range(1, length):
            if length % i == 0:
                factors.append(i)
        
        factors_dict[length] = factors
    
    
    return factors_dict

def get_invalid_ids_rule_2(all_ids):
    # invalid is a sequence of numbers that repeats at least twice
    # now does not have to be even length
    # can be anywhere in string
    invalid_ids = []
    factors_dict = get_factors_dict(all_ids)
    for i in range(len(all_ids)):
        this_id = str(all_ids[i])
        this_id_length = len(this_id)
        these_factors = factors_dict[this_id_length]


        #loop through first half of factors
        for j, factor in enumerate(these_factors):
            paired_factor = this_id_length // factor
            # Get the first factor characters
            first_factor_chars = this_id[:factor]
            # Check if this pattern repeats paired_factor number of times
            expected_pattern = first_factor_chars * paired_factor
            if this_id == expected_pattern:
                invalid_ids.append(all_ids[i])
                break  # Found invalid, no need to check other factors
        
    
    np.array(invalid_ids)
    return invalid_ids


all_ids = read_input('real_input.csv')
invalid_ids_rule_1 = get_invalid_ids_rule_1(all_ids)
sum_invalid_ids_rule_1 = np.sum(invalid_ids_rule_1)
print(f"invalid_ids_rule_1: {invalid_ids_rule_1}")
print(f"sum_invalid_ids_rule_1: {sum_invalid_ids_rule_1}") 

invalid_ids_rule_2 = get_invalid_ids_rule_2(all_ids)
sum_invalid_ids_rule_2 = np.sum(invalid_ids_rule_2)
print(f"invalid_ids_rule_2: {invalid_ids_rule_2}")
print(f"sum_invalid_ids_rule_2: {sum_invalid_ids_rule_2}")


