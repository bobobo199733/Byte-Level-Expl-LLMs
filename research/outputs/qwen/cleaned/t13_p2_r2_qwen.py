def spiral_matrix(matrix):
    if not matrix or not matrix[0]:
        return []
    rows, cols = (len(matrix), len(matrix[0]))
    result = []
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    visited = set()
    row, col, direction_idx = (0, 0, 0)
    while len(visited) < rows * cols:
        if (row, col) not in visited:
            result.append(matrix[row][col])
            visited.add((row, col))
        next_row, next_col = (row + directions[direction_idx][0], col + directions[direction_idx][1])
        if 0 <= next_row < rows and 0 <= next_col < cols and ((next_row, next_col) not in visited):
            row, col = (next_row, next_col)
        else:
            direction_idx = (direction_idx + 1) % 4
            row += directions[direction_idx][0]
            col += directions[direction_idx][1]
    return result