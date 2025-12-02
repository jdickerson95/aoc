
def read_turn_file(file_path):
    with open(file_path, 'r') as file:
        return [line.rstrip('\n') for line in file]

def get_wrapped_index(index, size):
    return index % size

def decode_turn(turn_string):
    letter = turn_string[0]
    steps = int(turn_string[1:])
    if letter == 'L':
        return -steps
    return steps

def get_num_zero_clicks(index, size, current_index, step):
    num_clicks = 0
    if step >= 0:
        num_clicks = index // size
    else:
        apparent_index = 100 - current_index
        num_clicks = (apparent_index-step) // size
        if current_index == 0:
            num_clicks -= 1
    return num_clicks



list_size = 100
current_index = 50
zero_counts = 0
num_zero_clicks = 0

turns = read_turn_file('turn_file.txt')
for turn in turns:
    step = decode_turn(turn)
    new_index = current_index + step
    num_zero_clicks_new = get_num_zero_clicks(new_index, list_size, current_index, step)
    num_zero_clicks += num_zero_clicks_new
    current_index = get_wrapped_index(new_index, list_size)
    print(f"turn {turn}: full_index: {new_index}, wrap_index: {current_index}, zero clicks: {num_zero_clicks_new}")
    if current_index == 0:
        zero_counts += 1

print(f"Zero counts: {zero_counts}")
print(f"Number of zero passes: {num_zero_clicks}")
