def sudoku_solver(board):
    """
    Solves a Sudoku puzzle in-place.

    Args:
        board (list): A 2D list representing the Sudoku board.
            Each inner list represents a row, and each element
            in the inner list is an integer between 1 and 9,
            or 0 if the cell is empty.

    Returns:
        bool: True if the puzzle was solved successfully, False otherwise.
    """

    def is_valid(num, row, col):
        """Check if a number can be placed at a given position."""
        for x in range(9):
            if board[row][x] == num:
                return False
        for x in range(9):
            if board[x][col] == num:
                return False
        start_row, start_col = (row - row % 3, col - col % 3)
        for i in range(3):
            for j in range(3):
                if board[i + start_row][j + start_col] == num:
                    return False
        return True

    def solve():
        """Solve the Sudoku puzzle recursively."""
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if is_valid(num, row, col):
                            board[row][col] = num
                            if solve():
                                return True
                            board[row][col] = 0
                    return False
        return True
    return solve()