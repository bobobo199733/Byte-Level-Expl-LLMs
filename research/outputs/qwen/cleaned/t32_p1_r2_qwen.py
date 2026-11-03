def n_queens(n):

    def is_safe(board, row, col):
        for i in range(col):
            if board[row][i]:
                return False
        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if board[i][j]:
                return False
        for i, j in zip(range(row, n, 1), range(col, -1, -1)):
            if board[i][j]:
                return False
        return True

    def solve(board, col):
        if col >= n:
            result.append([''.join(('Q' if x else '.' for x in row)) for row in board])
            return
        for i in range(n):
            if is_safe(board, i, col):
                board[i][col] = 1
                solve(board, col + 1)
                board[i][col] = 0
    result = []
    initial_board = [[0] * n for _ in range(n)]
    solve(initial_board, 0)
    return result