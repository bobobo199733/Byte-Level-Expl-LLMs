def spiral_matrix(matrix):
    if not matrix or not matrix:
        return []
    direction = 0
    row_start, col_start, row_end, col_end = (0, 0, len(matrix) - 1, len(matrix[0]) - 1)
    result = []
    while row_start <= row_end and col_start <= col_end:
        if direction == 0:
            for i in range(col_start, col_end + 1):
                result.append(matrix[row_start][i])
            row_start += 1
        if direction == 1:
            for i in range(row_start, row_end + 1):
                if col_end - col_start + 1 < row_end - row_start + 1:
                    result.append(matrix[i][col_end])
                    col_end -= 1
                else:
                    for j in range(row_start, row_end + 1):
                        result.append(matrix[j][col_end])
                    direction = 2
        if direction == 2:
            for i in range(row_end, row_start - 1, -1):
                if col_end - col_start + 1 > row_end - row_start:
                    result.append(matrix[i][col_start])
                    col_start += 1
                else:
                    for j in range(col_start, col_end + 1, -1):
                        result.append(matrix[row_end][j])
                    direction = 3
        if direction == 3:
            for i in range(col_end, col_start - 1, -1):
                if col_end - col_start + 1 > row_end - row_start:
                    result.append(matrix[row_end][i])
                    row_end -= 1
                else:
                    for j in range(row_end, row_start - 1, -1):
                        result.append(matrix[j][col_start])
                    direction = 0
    return result