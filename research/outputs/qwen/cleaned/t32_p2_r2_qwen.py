def n_queens(n):

    def is_safe(board, row, col):
        for i in range(col):
            if board[row][i] == 1:
                return False
        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if board[i][j] == 1:
                return False
        for i, j in zip(range(row, n, 1), range(col, -1, -1)):
            if board[i][j] == 1:
                return False
        return True

    def solve_n_queens_util(board, col):
        if col >= n:
            solutions.append([board[i][:] for i in range(n)])
            return
        for i in range(n):
            if is_safe(board, i, col):
                board[i][col] = 1
                solve_n_queens_util(board, col + 1)
                board[i][col] = 0

    def initialize_board(n):
        return [[0 for _ in range(n)] for _ in range(n)]
    solutions = []
    if n == 0 or n == 1:
        return solutions
    board = initialize_board(n)
    solve_n_queens_util(board, 0)
    return solutions