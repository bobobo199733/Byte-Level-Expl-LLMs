def n_queens(n):

    def place_queens(row=0):
        if row == n:
            yield board
        else:
            for col in range(n):
                if not conflicts_in_row(board, row, col) and (not conflicts_on_diagonal(board, row, col)):
                    board[row] = col
                    if place_queens(row + 1):
                        yield board
            board[row] = -1
    board = [-1] * n
    for solution in place_queens():
        yield solution

def conflicts_in_row(board, row, col):
    return any((board[r] == col for r in range(row)))

def conflicts_on_diagonal(board, row, col):
    return any((abs(board[r] - col) == abs(row - r) for r in range(row)))