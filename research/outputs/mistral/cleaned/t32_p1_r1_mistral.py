def is_valid(board, col):
    for i in range(col):
        if board[col] == board[i] or abs(board[col] - board[i]) == abs(col - i):
            return False
    return True

def n_queens(n):

    def backtrack(row, queens):
        if row >= n:
            yield tuple(queens)
            return
        for col in range(n):
            new_queens = queens[:]
            new_queens[row] = col
            if is_valid(new_queens, col):
                backtrack(row + 1, new_queens)
    backtrack(0, [-1] * n)