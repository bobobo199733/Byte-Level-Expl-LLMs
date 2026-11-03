def matrix_multiply(A, B):
    if len(A) != len(B[0]):
        raise ValueError('Matrix dimensions are incompatible.')
    result = [[0] * len(B[0][0]) for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(A[0])):
                result[i][j] += A[i][k] * B[k][j]
    return result