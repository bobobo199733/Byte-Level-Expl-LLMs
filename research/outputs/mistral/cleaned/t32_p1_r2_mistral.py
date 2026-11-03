def n_queens(n):

    def is_safe(board, row, col):
        for i in range(row):
            if board[i] == col or abs(board[i] - col) == abs(i - row):
                return False
        return True

    def solve_n_queens(n, solutions, board=[-1] * n, row=0):
        if row == n:
            solutions.append([str(x) for x in board])
            return
        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                solve_n_queens(n, solutions, board, row + 1)
    solutions = []
    solve_n_queens(n, solutions)
    return solutions