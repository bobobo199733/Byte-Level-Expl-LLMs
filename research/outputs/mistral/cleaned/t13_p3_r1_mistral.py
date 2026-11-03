def spiral_order(matrix):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    visited = set()
    result = []
    row, col = (len(matrix), len(matrix[0]))
    r, c, d = (0, 0, 0)
    while r < row and c < col:
        visited.add((r, c))
        x, d = (r + directions[d][0], (d + 1) % len(directions))
        if 0 <= x < row and (x, c) not in visited:
            r, c = (x, c)
        else:
            r, c = (r, c + 1)
    return list(result) + list((matrix[i][j] for i, row in enumerate(matrix) for j, _ in enumerate(row) if (i, j) not in visited))