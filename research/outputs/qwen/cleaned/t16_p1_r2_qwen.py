def is_valid(board, row, col, num):
    for x in range(9):
        if board[row][x] == num:
            return False
    for y in range(9):
        if board[y][col] == num:
            return False
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False
    return True

def solve_sudoku(board):

    def backtrack():
        nonlocal board
        for row in range(9):
            for col in range(9):
                if board[row][col] == '.':
                    for num in '123456789':
                        if is_valid(board, row, col, num):
                            board[row][col] = num
                            if backtrack():
                                return True
                            board[row][col] = '.'
                    return False
        return True
    for row in range(9):
        for col in range(9):
            if board[row][col] == '.':
                board[row][col] = '0'
    solve_sudoku_helper(board)
    for row in range(9):
        for col in range(9):
            if board[row][col] == '0':
                board[row][col] = '.'

def sudoku_solver(board):
    return solve_sudoku(board)