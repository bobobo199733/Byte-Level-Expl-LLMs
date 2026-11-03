def matrix_multiply(A, B):
    """
    Multiplies two matrices A and B.

    Args:
        A (list of lists): The first matrix.
        B (list of lists): The second matrix.

    Returns:
        list of lists: The resulting matrix from multiplying A and B.
    """
    assert len(A[0]) == len(B), 'Incompatible matrices for multiplication'
    num_rows_A = len(A)
    num_cols_B = len(B[0])
    num_cols_A = len(A[0])
    C = [[0] * num_cols_B for _ in range(num_rows_A)]
    for i in range(num_rows_A):
        for j in range(num_cols_B):
            for k in range(num_cols_A):
                C[i][j] += A[i][k] * B[k][j]
    return C