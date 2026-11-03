def is_valid_move(board, row, col, num):
    for x in range(9):
        if board[row][x] == num:
            return False
        if board[x][col] == num:
            return False
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False
    return True

def find_empty_location(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return (row, col)
    return None

def sudoku_solver(board):
    empty_loc = find_empty_location(board)
    if not empty_loc:
        return True
    row, col = empty_loc
    for num in range(1, 10):
        if is_valid_move(board, row, col, num):
            board[row][col] = num
            if sudoku_solver(board):
                return True
            board[row][col] = 0
    raise ValueError('Unsolvable Sudoku puzzle')