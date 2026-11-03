def spiral_matrix(matrix):
    """
    Returns all elements of a 2D matrix in spiral order.

    Args:
        matrix (list): A 2D list representing a square or rectangular matrix.

    Returns:
        list: A 1D list containing all elements of the input matrix in spiral order.
    """
    num_rows = len(matrix)
    if num_rows == 0:
        return []
    num_cols = len(matrix[0])
    top = 0
    bottom = num_rows - 1
    left = 0
    right = num_cols - 1
    result = []
    while True:
        for i in range(left, right + 1):
            result.append(matrix[top][i])
        top += 1
        if top > bottom or left > right:
            break
        for i in range(top, bottom + 1):
            result.append(matrix[i][right])
        right -= 1
        if top > bottom or left > right:
            break
        if top <= bottom:
            for i in range(right, left - 1, -1):
                result.append(matrix[bottom][i])
            bottom -= 1
            if top > bottom or left > right:
                break
        if left <= right:
            for i in range(bottom, top - 1, -1):
                result.append(matrix[i][left])
            left += 1
            if top > bottom or left > right:
                break
    return result