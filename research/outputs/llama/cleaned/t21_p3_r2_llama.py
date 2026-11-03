def matrix_multiply(A, B):
    """
    Multiply two matrices A and B.

    Args:
        A (list of lists): The first matrix.
        B (list of lists): The second matrix.

    Returns:
        list of lists: The product of A and B.
    """
    if len(A[0]) != len(B):
        raise ValueError('The number of columns in A must be equal to the number of rows in B')
    num_rows_A = len(A)
    num_cols_B = len(B[0])
    C = [[0 for _ in range(num_cols_B)] for _ in range(num_rows_A)]
    for i in range(num_rows_A):
        for j in range(num_cols_B):
            C[i][j] = sum((A[k][j] * B[i][k] for k in range(len(B))))
    return C