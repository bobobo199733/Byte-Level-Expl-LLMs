def n_queens(n):

    def is_safe(board, row, col):
        for i in range(row):
            if board[i] == col or abs(board[i] - col) == abs(i - row):
                return False
        return True

    def solve(row):
        if row > n:
            yield tuple(board)
            return
        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                solve(row + 1)
                board[row] = -1
    board = [-1] * n
    solve(0)