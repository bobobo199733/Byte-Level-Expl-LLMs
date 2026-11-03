def matrix_multiply(A, B):
    """Return the product of two matrices A and B.

    Args:
        A (list of lists): The first matrix.
        B (list of lists): The second matrix.

    Returns:
        list of lists: The product of matrices A and B.

    Raises:
        ValueError: If the dimensions of A and B are incompatible for multiplication.
    """
    if not all((isinstance(row, list) for row in A)):
        raise TypeError('Matrix A should be a list of lists')
    if not all((isinstance(row, list) for row in B)):
        raise TypeError('Matrix B should be a list of lists')
    num_rows_A = len(A)
    num_cols_B = len(B[0])
    num_cols_A = len(A[0])
    if not all((len(row) == num_cols_A for row in A)):
        raise ValueError('Matrix dimensions are incompatible')
    if not (num_rows_A == num_cols_B and num_cols_A == num_cols_B):
        raise ValueError('Matrix dimensions are incompatible')
    C = [[0] * num_cols_B for _ in range(num_rows_A)]
    for i in range(num_rows_A):
        for j in range(num_cols_B):
            for k in range(num_cols_A):
                C[i][j] += A[i][k] * B[k][j]
    return C