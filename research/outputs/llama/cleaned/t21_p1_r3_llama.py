def matrix_multiply(A, B):
    """
    Multiply two matrices A and B.

    Args:
        A (list of lists): The first matrix.
        B (list of lists): The second matrix.

    Returns:
        list of lists: The product of the input matrices.

    Raises:
        ValueError: If the number of columns in A does not match the number of rows in B.
    """
    num_rows_A = len(A)
    num_cols_A = len(A[0])
    num_rows_B = len(B)
    num_cols_B = len(B[0])
    if num_cols_A != num_rows_B:
        raise ValueError('Number of columns in A does not match number of rows in B')
    result = [[0 for _ in range(num_cols_B)] for _ in range(num_rows_A)]
    for i in range(num_rows_A):
        for j in range(num_cols_B):
            for k in range(num_cols_A):
                result[i][j] += A[i][k] * B[k][j]
    return result