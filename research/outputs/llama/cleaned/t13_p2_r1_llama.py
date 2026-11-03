def spiral_matrix(matrix):
    """
    Traverse a matrix in spiral order and return visited elements as a list.

    Args:
        matrix (list of lists): A 2D list representing the matrix.

    Returns:
        list: A list of visited elements.
    """
    if not matrix or not any(matrix):
        return []
    rows, cols = (len(matrix), len(matrix[0]))
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    result = []
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    dir_index = 0
    row, col = (0, 0)
    while len(result) < rows * cols:
        visited[row][col] = True
        result.append(matrix[row][col])
        next_row, next_col = (row + directions[dir_index][0], col + directions[dir_index][1])
        if next_row >= 0 and next_row < rows and (next_col >= 0) and (next_col < cols) and (not visited[next_row][next_col]):
            row, col = (next_row, next_col)
        else:
            dir_index = (dir_index + 1) % 4
        row += directions[dir_index][0]
        col += directions[dir_index][1]
    return result