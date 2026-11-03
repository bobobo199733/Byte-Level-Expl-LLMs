def spiral_matrix(matrix):
    """
    Returns all elements of a 2D matrix in spiral order.

    Args:
        matrix (list): A 2D list representing the input matrix.

    Returns:
        list: A 1D list containing all elements of the input matrix in spiral order.
    """
    result = []
    top = 0
    bottom = len(matrix) - 1
    left = 0
    right = len(matrix[0]) - 1
    while top <= bottom and left <= right:
        for i in range(left, right + 1):
            result.append(matrix[top][i])
        top += 1
        for i in range(top, bottom + 1):
            result.append(matrix[i][right])
        right -= 1
        if top > bottom or left > right:
            break
        for i in range(right, left - 1, -1):
            result.append(matrix[bottom][i])
        bottom -= 1
        for i in range(bottom, top - 1, -1):
            result.append(matrix[i][left])
        left += 1
    return result