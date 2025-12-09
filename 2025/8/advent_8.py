import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components


def read_input(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    return lines

def input_to_array(lines):
    return np.array([[int(x) for x in line.strip().split(',')] for line in lines])

def compute_distances(array):
    # Compute all pairwise differences using broadcasting
    # array[:, None, :] has shape (N, 1, 3)
    # array[None, :, :] has shape (1, N, 3)
    # Result has shape (N, N, 3) - all pairwise differences
    diff = array[:, None, :] - array[None, :, :]
    
    # Compute Euclidean distance for all pairs: shape (N, N)
    dist_matrix = np.linalg.norm(diff, axis=2)
    
    return dist_matrix

def n_smallest_distances(dist_matrix, n):
    # Mask out diagonal and lower triangle (only consider upper triangle)
    masked_matrix = dist_matrix.copy()
    masked_matrix[np.tril_indices_from(masked_matrix)] = np.inf  # Mask lower triangle + diagonal
    
    # Flatten the matrix and find n smallest values
    flat_distances = masked_matrix.flatten()
    flat_indices = np.argpartition(flat_distances, n)[:n]
    flat_indices = flat_indices[np.argsort(flat_distances[flat_indices])]
    
    # Convert flat indices back to 2D indices
    n_points = dist_matrix.shape[0]
    row_indices = flat_indices // n_points
    col_indices = flat_indices % n_points
    indices = np.column_stack([row_indices, col_indices])
    
    # Get the corresponding distances
    distances = flat_distances[flat_indices]
    
    return distances, indices


def find_circuits(indices, n_points):
    # Build adjacency matrix
    row = indices[:, 0]
    col = indices[:, 1]
    # Make it symmetric (undirected graph)
    data = np.ones(len(indices) * 2)
    adj_row = np.concatenate([row, col])
    adj_col = np.concatenate([col, row])
    
    # Create sparse adjacency matrix
    adj_matrix = csr_matrix((data, (adj_row, adj_col)), shape=(n_points, n_points))
    
    # Find connected components
    n_circuits, labels = connected_components(adj_matrix, directed=False)

    # Count points in each circuit
    circuit_sizes = [np.sum(labels == i) for i in range(n_circuits)]
    
    return n_circuits, circuit_sizes

def product_of_largest_circuits(circuit_sizes, largest_n):
    sorted_sizes = np.sort(circuit_sizes)[::-1]  # Sort descending
    largest = sorted_sizes[:largest_n]
    return np.prod(largest)

def min_connections_for_complete_circuit(dist_matrix, array):
    n_points = dist_matrix.shape[0]
    max_possible_connections = n_points * (n_points - 1) // 2  # Upper triangle size
    
    # Binary search for minimum connections
    left = 1
    right = max_possible_connections
    
    while left < right:
        mid = (left + right) // 2
        _, indices = n_smallest_distances(dist_matrix, mid)
        n_circuits, _ = find_circuits(indices, n_points)
        
        if n_circuits == 1:
            # All points are connected, try fewer connections
            right = mid
        else:
            # Not all points connected, need more connections
            left = mid + 1
    
    # Get the connections at the minimum number needed
    _, indices = n_smallest_distances(dist_matrix, left)
    # The last connection (largest distance) is the one that completed the circuit
    last_connection = indices[-1]
    last_connection_coords = array[last_connection]
    
    return left, last_connection_coords

lines = read_input('real_input.txt')
number_connections = 1000
number_largest_circuits = 3

array = input_to_array(lines)
dist_matrix = compute_distances(array)

## part 1
distances, indices = n_smallest_distances(dist_matrix, number_connections)
print(distances)
print(indices)
n_circuits, circuit_sizes = find_circuits(indices, array.shape[0])
product = product_of_largest_circuits(circuit_sizes, number_largest_circuits)
print(product)


## part 2
min_connections, last_connection_coords = min_connections_for_complete_circuit(dist_matrix, array)
print(f"Minimum connections for complete circuit: {min_connections}")
print(f"Last connection coordinates: {last_connection_coords}")
#print xcoord times xcoord
print(f"Product of x coords of last two coords: {last_connection_coords[0][0] * last_connection_coords[1][0]}")


