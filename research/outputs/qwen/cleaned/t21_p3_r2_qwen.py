def matrix_multiply(A, B):
    """
    Multiplies two matrices A and B.

    Parameters:
    A (list of lists): The first matrix.
    B (list of lists): The second matrix.

    Returns:
    list of lists: The resulting matrix after multiplication.

    Raises:
    ValueError: If the number of columns in A does not equal the number of rows in B.
    """
    if len(A[0]) != len(B):
        raise ValueError('The number of columns in A must equal the number of rows in B')
    result = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result