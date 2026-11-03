def sudoku_solver(board):
    """
    Solves a Sudoku puzzle using the backtracking algorithm.

    Args:
        board (list): A 2D list representing the Sudoku board.
            Each inner list should have 9 elements, and each element should be an integer between 1 and 9,
            or zero if the position is empty.

    Returns:
        bool: True if a solution was found, False otherwise.
    """
    find = find_empty(board)
    if not find:
        return True
    else:
        row, col = find
    for i in range(1, 10):
        if valid(board, i, (row, col)):
            board[row][col] = i
            if sudoku_solver(board):
                return True
            board[row][col] = 0
    return False

def valid(board, num, pos):
    """
    Checks if a number is valid in a given position on the Sudoku board.

    Args:
        board (list): A 2D list representing the Sudoku board.
        num (int): The number to check for validity.
        pos (tuple): The row and column indices of the position to check.

    Returns:
        bool: True if the number is valid in the given position, False otherwise.
    """
    for i in range(len(board[0])):
        if board[pos[0]][i] == num and pos[1] != i:
            return False
    for i in range(len(board)):
        if board[i][pos[1]] == num and pos[0] != i:
            return False
    box_x = pos[1] // 3
    box_y = pos[0] // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False
    return True

def find_empty(board):
    """
    Finds an empty position on the Sudoku board.

    Args:
        board (list): A 2D list representing the Sudoku board.

    Returns:
        tuple: The row and column indices of an empty position, or None if no empty positions are found.
    """
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)
    return None