def is_valid(row, col, num, board):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    box_x = row - row % 3
    box_y = col - col % 3
    for i in range(box_x, box_x + 3):
        for j in range(box_y, box_y + 3):
            if board[i][j] == num:
                return False
    return True

def sudoku_solver(board):
    empty_cells = find_empty_cells(board)
    for row, col in empty_cells:
        for num in range(1, 10):
            if is_valid(row, col, num, board):
                board[row][col] = num
                if sudoku_solver(board):
                    return True
            board[row][col] = 0
    return False

def find_empty_cells(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                yield (row, col)

def print_board(board):
    for row in board:
        for num in row:
            print(num, end=' ')
        print()
    print()