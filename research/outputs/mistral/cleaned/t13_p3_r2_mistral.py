def spiral_matrix(matrix):
    if not matrix or not matrix:
        return []
    top = 0
    bottom = len(matrix) - 1
    left = 0
    right = len(matrix[0]) - 1
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    result = []
    while True:
        for i in range(len(matrix[left])):
            result.append(matrix[top][left + i])
        top += 1
        if len(result) > (bottom - top + 1) * (right - left + 1):
            break
        for i in range(len(matrix)):
            result.append(matrix[top + i][right])
        left += 1
        if len(result) > (bottom - top + 1) * (right - left + 1):
            break
        for i in range(len(matrix[0])):
            result.append(matrix[bottom][right - i])
        bottom -= 1
        if len(result) > (bottom - top + 1) * (right - left + 1):
            break
        for i in range(len(matrix)):
            result.append(matrix[bottom - i][left])
        right -= 1
    return result