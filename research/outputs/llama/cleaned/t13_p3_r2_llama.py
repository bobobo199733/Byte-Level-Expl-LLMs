def spiral_matrix(matrix):
    """
    Returns the elements of a matrix in spiral order.

    Args:
        matrix (list): A 2D list representing the input matrix.

    Returns:
        list: A 1D list containing the elements of the matrix in spiral order.
    """
    result = []
    while matrix:
        result += matrix.pop(0)
        if matrix and matrix[0]:
            for row in matrix:
                result.append(row.pop())
            matrix = [list(reversed(col)) for col in zip(*matrix)]
    return result