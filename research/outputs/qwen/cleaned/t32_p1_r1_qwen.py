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
            result.append([''.join(row) for row in board])
            return
        for i in range(n):
            if is_safe(board, i, col):
                board[i][col] = 'Q'
                solve_n_queens(board, col + 1)
                board[i][col] = '.'
    result = []
    board = [['.' for _ in range(n)] for _ in range(n)]
    solve_n_queens(board, 0)
    return result