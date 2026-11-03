def is_valid(board, row, col, num):
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

def find_empty_location(board, pos):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                pos[0], pos[1] = (row, col)
                return True
    return False

def sudoku_solver(board):
    position = [0, 0]
    if not find_empty_location(board, position):
        return True
    row, col = (position[0], position[1])
    for num in range(1, 10):
        if is_valid(board, row, col, str(num)):
            board[row][col] = str(num)
            if sudoku_solver(board):
                return True
            board[row][col] = '0'
    return False