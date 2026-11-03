def spiral_matrix(matrix):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    result, row, col, direction = ([], 0, 0, 0)
    while True:
        x, y = (row + directions[direction][0], col + directions[direction][1])
        if 0 <= x < len(matrix) and 0 <= y < len(matrix[0]) and ((x, y) not in result):
            result.append(matrix[x][y])
            matrix[x][y] = visited = True
            row, col = (x, y)
        if visited:
            visited = False
            row, col, direction = (row, col, (direction + 1) % len(directions))
        elif not matrix[row + directions[(direction - 1) % len(directions)][0]][col + directions[(direction - 1) % len(directions)][1]]:
            break
    return result