def is_valid(board, row, col, num):
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

    def fill(row, col):
        if row == 9:
            return True
        for i in range(col, 9):
            if board[row][i] != '.':
                fill(row, i + 1)
            elif all((is_valid(board, row, i, num) for num in range(1, 10))):
                board[row][col] = str(num)
                if fill(row + 1, 0):
                    return True
                board[row][col] = '.'
        if not fill(row + 1, 0):
            board[row] = ['.'] * 9
            fill(row, 0)
    fill(0, 0)
    return board