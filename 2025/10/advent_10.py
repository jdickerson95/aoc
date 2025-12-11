import pulp
import numpy as np

def read_input(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    return lines

def parse_input(lines):
    """
    Parse input into three lists:
    1. Square brackets: list of 0 for '.' and 1 for '#'
    2. Parentheses: list of lists of numbers for each () group
    3. Curly brackets: list of numbers in {}
    """
    square_brackets = []
    parentheses = []
    curly_brackets = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Extract square brackets content
        sq_start = line.find('[')
        sq_end = line.find(']')
        if sq_start != -1 and sq_end != -1:
            sq_content = line[sq_start + 1:sq_end]
            # Convert '.' to 0 and '#' to 1
            sq_list = [0 if c == '.' else 1 for c in sq_content]
            square_brackets.append(sq_list)
        
        # Extract all parentheses groups
        paren_groups = []
        i = 0
        while i < len(line):
            if line[i] == '(':
                # Find matching closing parenthesis
                depth = 1
                j = i + 1
                while j < len(line) and depth > 0:
                    if line[j] == '(':
                        depth += 1
                    elif line[j] == ')':
                        depth -= 1
                    j += 1
                # Extract content between parentheses
                paren_content = line[i + 1:j - 1]
                # Parse comma-separated numbers
                if paren_content:
                    numbers = [int(x.strip()) for x in paren_content.split(',')]
                    paren_groups.append(numbers)
                i = j
            else:
                i += 1
        parentheses.append(paren_groups)
        
        # Extract curly brackets content
        curl_start = line.find('{')
        curl_end = line.find('}')
        if curl_start != -1 and curl_end != -1:
            curl_content = line[curl_start + 1:curl_end]
            # Parse comma-separated numbers
            numbers = [int(x.strip()) for x in curl_content.split(',')]
            curly_brackets.append(numbers)
    
    return square_brackets, parentheses, curly_brackets


def min_button_presses_part1(initial_state, target_state, buttons):
    initial = np.array(initial_state)
    target = np.array(target_state)
    b = (target ^ initial).astype(int)  # what flips we need
    
    n_buttons = len(buttons)
    n_coins = len(initial_state)

    # Build matrix A[i,j] = 1 if button j flips coin i
    A = np.zeros((n_coins, n_buttons), dtype=int)
    for j, flips in enumerate(buttons):
        for i in flips:
            A[i, j] = 1

    # Define LP
    prob = pulp.LpProblem("MinFlip", pulp.LpMinimize)

    # x[j] = whether we press button j (binary)
    x = pulp.LpVariable.dicts("x", range(n_buttons), lowBound=0, upBound=1, cat="Binary")

    # k[i] = integer slack for modulo equation
    k = pulp.LpVariable.dicts("k", range(n_coins), lowBound=0, cat="Integer")

    # objective: minimize number of presses
    prob += pulp.lpSum([x[j] for j in range(n_buttons)])

    # constraints: A x - 2 k = b
    for i in range(n_coins):
        prob += (
            pulp.lpSum(A[i, j] * x[j] for j in range(n_buttons))
            - 2 * k[i]
            == b[i]
        )

    # Solve
    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    # Extract solution
    chosen = [j for j in range(n_buttons) if pulp.value(x[j]) > 0.5]
    return chosen, len(chosen)

def part1(desired_states, all_buttons):
    num_presses = np.zeros(len(desired_states), dtype=int)
    for i,desired_state in enumerate(desired_states):
        buttons = all_buttons[i]
        initial_state = [0] * len(desired_state)
        _, num_presses[i] = min_button_presses_part1(initial_state, desired_state, buttons)
        print(f"Number of presses for desired state {i}: {num_presses[i]}")
    print(f"Total number of presses: {np.sum(num_presses)}")


lines = read_input('real_input.txt')
target_states, all_buttons, all_joltages = parse_input(lines)

print("Target states:")
for i, target_state in enumerate(target_states):
    print(f"  Line {i+1}: {target_state}")

print("All buttons:")
for i, buttons in enumerate(all_buttons):
    print(f"  Line {i+1}: {buttons}")

part1(target_states, all_buttons)


def min_add_button_presses_part2(initial, target, buttons):
    """
    Solve the problem where pressing button j adds 1 to each listed coin index.
    Returns: (press_counts_list, total_presses)
    """

    initial = np.array(initial, dtype=int)
    target  = np.array(target,  dtype=int)
    b = target - initial
    n = len(initial)
    m = len(buttons)

    # Build matrix A where A[i,j] = 1 if button j affects coin i
    A = np.zeros((n, m), dtype=int)
    for j, flips in enumerate(buttons):
        for i in flips:
            A[i, j] += 1   # or += 1 for multiple adds per press

    # ILP problem
    prob = pulp.LpProblem("button_addition", pulp.LpMinimize)

    # Variables x_j = # times to press button j (must be non-negative integers)
    x = [pulp.LpVariable(f"x{j}", lowBound=0, cat=pulp.LpInteger) for j in range(m)]

    # Objective: minimize total presses
    prob += sum(x)

    # Constraints: A x = b
    for i in range(n):
        prob += sum(A[i, j] * x[j] for j in range(m)) == b[i]

    # Solve
    status = prob.solve(pulp.PULP_CBC_CMD(msg=False))

    if pulp.LpStatus[status] != "Optimal":
        return None

    # Extract solution
    presses = [int(x[j].value()) for j in range(m)]
    total = sum(presses)
    return presses, total


def part2(target_states, all_buttons):
    num_presses = np.zeros(len(target_states), dtype=int)
    for i,target_state in enumerate(target_states):
        buttons = all_buttons[i]
        initial_state = [0] * len(target_state)
        _, num_presses[i] = min_add_button_presses_part2(initial_state, target_state, buttons)
        print(f"Number of presses for target state {i}: {num_presses[i]}")
    print(f"Total number of presses: {np.sum(num_presses)}")

part2(all_joltages, all_buttons)

