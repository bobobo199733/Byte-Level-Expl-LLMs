def is_valid(board, row, col, num):
    """
    Checks if it's possible to place a number at the given position on the board.

    :param board: The Sudoku board.
    :param row: The row index.
    :param col: The column index.
    :param num: The number to check.
    :return: True if the number can be placed, False otherwise.
    """
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    start_row = row - row % 3
    start_col = col - col % 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def sudoku_solver(board):
    """
    Solves a Sudoku puzzle in-place using backtracking.

    :param board: The Sudoku board.
    """
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if sudoku_solver(board):
                            return True
                        else:
                            board[row][col] = 0
                return False
    return True