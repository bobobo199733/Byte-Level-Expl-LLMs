def matrix_multiply(A, B):
    if not all((isinstance(row, list) for row in A)) or not all((isinstance(row, list) for row in B)):
        raise TypeError('Inputs must be lists of lists')
    num_rows_A = len(A)
    num_cols_A = len(A[0])
    num_rows_B = len(B)
    num_cols_B = len(B[0])
    if num_cols_A != num_rows_B:
        raise ValueError('Matrix dimensions are incompatible for multiplication')
    C = [[0] * num_cols_B for _ in range(num_rows_A)]
    for i in range(num_rows_A):
        for j in range(num_cols_B):
            for k in range(num_rows_B):
                C[i][j] += A[i][k] * B[k][j]
    return C