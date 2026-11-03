def spiral_matrix(matrix):
    """
    Returns a list of visited elements in a matrix, traversed in spiral order.

    Args:
        matrix (list): A 2D list representing the matrix to traverse.

    Returns:
        list: The visited elements in the matrix.
    """
    if not matrix or not all((row for row in matrix)):
        return []
    rows, cols = (len(matrix), len(matrix[0]))
    visited = set()
    result = []
    top, bottom = (0, rows - 1)
    left, right = (0, cols - 1)
    while top <= bottom and left <= right:
        for col in range(left, right + 1):
            if (top, col) not in visited:
                result.append(matrix[top][col])
                visited.add((top, col))
        top += 1
        for row in range(top, bottom + 1):
            if (row, right) not in visited:
                result.append(matrix[row][right])
                visited.add((row, right))
        right -= 1
        if top <= bottom:
            for col in range(right, left - 1, -1):
                if (bottom, col) not in visited:
                    result.append(matrix[bottom][col])
                    visited.add((bottom, col))
            bottom -= 1
        if left <= right:
            for row in range(bottom, top - 1, -1):
                if (row, left) not in visited:
                    result.append(matrix[row][left])
                    visited.add((row, left))
            left += 1
    return result