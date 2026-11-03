def is_valid(row, col, num, board):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num or (row - row % 3 + i // 3 < 9 and board[(row - row % 3 + i // 3) // 3 * 3 + i % 3][(col - col % 3 + i // 3) // 3 * 3 + i % 3] == num):
            return False
    return True

def find_empty(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return (row, col)
    return None

def sudoku_solver(board):
    empty = find_empty(board)
    if not empty:
        return True
    row, col = empty
    for num in range(1, 10):
        if is_valid(row, col, num, board):
            board[row][col] = num
            if sudoku_solver(board):
                return True
            board[row][col] = 0
    return False