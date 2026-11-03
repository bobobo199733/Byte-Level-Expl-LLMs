def is_valid(row, col, num, board):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    start_row = (row - row % 3) // 3
    start_col = (col - col % 3) // 3
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False
    return True

def sudoku_solver(board):

    def solve(row=0):
        for col in range(9):
            if board[row][col] != '.':
                continue
            for num in range(1, 10):
                if not is_valid(row, col, num, board):
                    continue
                board[row][col] = str(num)
                if row == 8:
                    return True
                if solve(row + 1):
                    return True
            board[row][col] = '.'
        return False
    if not solve():
        return 'No solution found'
    return board