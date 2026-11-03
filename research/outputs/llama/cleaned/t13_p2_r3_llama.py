def spiral_matrix(matrix):
    """
    Traverse a matrix in spiral order and return visited elements as a list.

    Args:
        matrix (list): A 2D list representing the matrix to traverse.

    Returns:
        list: The elements visited during traversal, in spiral order.
    """
    if not matrix or not any(matrix):
        return []
    rows, cols = (len(matrix), len(matrix[0]))
    visited = [[False] * cols for _ in range(rows)]
    result = []
    top, bottom, left, right = (0, rows - 1, 0, cols - 1)
    while top <= bottom and left <= right:
        for i in range(left, right + 1):
            if not visited[top][i]:
                result.append(matrix[top][i])
                visited[top][i] = True
        top += 1
        for i in range(top, bottom + 1):
            if not visited[i][right]:
                result.append(matrix[i][right])
                visited[i][right] = True
        right -= 1
        if top <= bottom:
            for i in range(right, left - 1, -1):
                if not visited[bottom][i]:
                    result.append(matrix[bottom][i])
                    visited[bottom][i] = True
            bottom -= 1
        if left <= right:
            for i in range(bottom, top - 1, -1):
                if not visited[i][left]:
                    result.append(matrix[i][left])
                    visited[i][left] = True
            left += 1
    return result