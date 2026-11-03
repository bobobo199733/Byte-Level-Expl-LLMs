def spiral_matrix(matrix):
    if not matrix or not matrix:
        return []
    rows, cols = (len(matrix), len(matrix[0]))
    traversed = []
    top, bottom = (0, rows - 1)
    left, right = (0, cols - 1)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    direction_idx = 0
    while traversed < rows * cols:
        traversed.append(matrix[top][left])
        next_pos_x, next_pos_y = (left + directions[direction_idx][0], top + directions[direction_idx][1])
        if next_pos_x < 0 or next_pos_x > right or next_pos_y < 0 or (next_pos_y > bottom) or (matrix[next_pos_y][next_pos_x] in traversed):
            direction_idx = (direction_idx + 1) % len(directions)
        left += directions[direction_idx][0]
        top += directions[direction_idx][1]
    return traversed