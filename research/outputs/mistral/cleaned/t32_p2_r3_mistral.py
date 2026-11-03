def is_safe(mat, row, col):
    for i in range(row):
        if mat[i][col] == 1:
            return False
    for i, j in enumerate(mat[row]):
        if i != col and mat[i][j] == 1:
            return False
    for i, j in enumerate([row - col + i, row + col + i]):
        if 0 <= i < len(mat) and j >= 0 and (j < len(mat[0])) and (mat[i][j] == 1):
            return False
    return True

def n_queens(n):
    if n <= 0:
        yield []
        return
    solutions = set()
    for i in range(n):
        board = [[0] * n for _ in range(n)]
        if is_safe(board, i, 0):
            board[i][0] = 1
            expanded_solutions = (sol + [list(board[j]) for j in range(n)] for sol in n_queens(n - 1))
            solutions.update(expanded_solutions)
    yield list((list(_)[0] for _ in solutions))