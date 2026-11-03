def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num:
            return False
    for i in range(9):
        if board[i][col] == num:
            return False
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def sudoku_solver(board):

    def solve_recursive(row, col):
        if row >= 9:
            return True
        for i in range(9):
            if is_valid(board, row, col, i + 1):
                board[row][col] = i + 1
                if solve_recursive(row + 1, col):
                    return True
                board[row][col] = 0
        return False
    return solve_recursive(0, 0)