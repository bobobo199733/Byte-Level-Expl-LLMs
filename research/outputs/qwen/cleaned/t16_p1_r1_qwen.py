def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num:
            return False
    for i in range(9):
        if board[i][col] == num:
            return False
    start_row, start_col = (3 * (row // 3), 3 * (col // 3))
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False
    return True

def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == '.' or board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, str(num)):
                        board[row][col] = str(num)
                        if solve_sudoku(board):
                            return True
                        board[row][col] = '.'
    return True

def sudoku_solver(board):
    global original_board
    original_board = board.copy()
    if solve_sudoku(original_board):
        for i in range(9):
            for j in range(9):
                board[i][j] = original_board[i][j]
        return True
    else:
        return False