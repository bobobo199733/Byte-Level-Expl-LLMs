def spiral_matrix(matrix):
    if not matrix or not matrix[0]:
        return []
    result = []
    rows, cols = (len(matrix), len(matrix[0]))
    top, bottom, left, right = (0, rows - 1, 0, cols - 1)
    while top <= bottom and left <= right:
        for i in range(left, right + 1):
            result.append(matrix[top][i])
        if top < bottom:
            for i in range(top + 1, bottom + 1):
                result.append(matrix[i][right])
        if bottom > top:
            for i in range(right - 1, left - 1, -1):
                result.append(matrix[bottom][i])
        if bottom > top + 1:
            for i in range(bottom - 1, top, -1):
                result.append(matrix[i][left])
        top += 1
        bottom -= 1
        left += 1
        right -= 1
    return result