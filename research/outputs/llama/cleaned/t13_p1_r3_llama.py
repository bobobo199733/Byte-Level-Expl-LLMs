def spiral_matrix(matrix):
    """
    Returns the elements of a 2D matrix in spiral order.

    Args:
        matrix (list): A 2D list representing the matrix.

    Returns:
        list: A list containing the elements of the matrix in spiral order.
    """
    result = []
    while matrix:
        result += matrix.pop(0)
        if matrix and matrix[0]:
            matrix = list(zip(*matrix))[::-1]
    return result