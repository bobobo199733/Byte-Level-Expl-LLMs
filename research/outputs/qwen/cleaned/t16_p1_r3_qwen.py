def is_valid(board, row, col, num):
    for x in range(9):
        if board[row][x] == num:
            return False
        if board[x][col] == num:
            return False
    start_row = row // 3 * 3
    start_col = col // 3 * 3
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False
    return True

def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == '.':
                for num in '123456789':
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = '.'
                return False
    return True

def sudoku_solver(board):
    solve_sudoku(board)