def n_queens(n):

    def is_safe(board, row, col):
        for i in range(col):
            if board[row][i] == 'Q':
                return False
        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if board[i][j] == 'Q':
                return False
        for i, j in zip(range(row, n, 1), range(col, -1, -1)):
            if board[i][j] == 'Q':
                return False
        return True

    def solve_n_queens(board, col):
        if col >= n:
            solutions.append([''.join(row) for row in board])
            return True
        res = False
        for i in range(n):
            if is_safe(board, i, col):
                board[i][col] = 'Q'
                res = solve_n_queens(board, col + 1) or res
                board[i][col] = '.'
        return res
    solutions = []
    board = [['.' for _ in range(n)] for _ in range(n)]
    solve_n_queens(board, 0)
    return solutions