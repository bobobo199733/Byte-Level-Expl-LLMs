def spiral_matrix(matrix):
    if not matrix or not matrix:
        return []
    rows, cols = (len(matrix), len(matrix[0]))
    direction = 0
    visited = [[False] * cols for _ in range(rows)]
    result = []
    x, y = (0, 0)
    while len(result) < rows * cols:
        visited[x][y] = True
        result.append(matrix[x][y])
        next_x, next_y = (x, y)
        if direction == 0:
            if y + 1 < cols and (not visited[x][y + 1]):
                next_x, next_y = (x, y + 1)
            else:
                direction += 1
        elif direction == 1:
            if x + 1 < rows and (not visited[x + 1][y]):
                next_x, next_y = (x + 1, y)
            else:
                direction += 1
        elif direction == 2:
            if y - 1 >= 0 and (not visited[x][y - 1]):
                next_x, next_y = (x, y - 1)
            else:
                direction += 1
        elif direction == 3:
            if x - 1 >= 0 and (not visited[x - 1][y]):
                next_x, next_y = (x - 1, y)
            else:
                x, y = (next_x, next_y)
                direction = (direction + 1) % 4
    return result