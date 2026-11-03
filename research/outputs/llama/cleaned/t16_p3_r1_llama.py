def is_valid(board, row, col, num):
    """
    Check if it's possible to place a number in the given position.
    
    Args:
        board (list): The Sudoku board.
        row (int): The row index.
        col (int): The column index.
        num (int): The number to be placed.
    
    Returns:
        bool: Whether the placement is valid or not.
    """
    for x in range(9):
        if board[row][x] == num or board[x][col] == num:
            return False
    start_row, start_col = (row - row % 3, col - col % 3)
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False
    return True

def sudoku_solver(board):
    """
    Solve a Sudoku puzzle using backtracking.
    
    Args:
        board (list): The Sudoku board.
    
    Returns:
        bool: Whether the puzzle is solvable or not.
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