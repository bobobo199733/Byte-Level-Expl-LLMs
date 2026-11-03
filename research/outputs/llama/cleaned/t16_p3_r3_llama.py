def is_valid(board, row, col, num):
    """
    Check if it's possible to place a number in a given position.

    Args:
        board (list): The Sudoku board.
        row (int): The current row index.
        col (int): The current column index.
        num (int): The number to be placed.

    Returns:
        bool: Whether the placement is valid or not.
    """
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False
    start_row, start_col = (row - row % 3, col - col % 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False
    return True

def sudoku_solver(board):
    """
    Solve the Sudoku puzzle using backtracking.

    Args:
        board (list): The Sudoku board.

    Returns:
        bool: Whether a solution was found or not.
    """
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                for num in range(1, 10):
                    if is_valid(board, i, j, num):
                        board[i][j] = num
                        if sudoku_solver(board):
                            return True
                        else:
                            board[i][j] = 0
                return False
    return True

def print_board(board):
    """
    Print the Sudoku board in a formatted way.

    Args:
        board (list): The Sudoku board.
    """
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print('- - - - - - - - - - -')
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print('| ', end='')
            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + ' ', end='')