def sudoku_solver(board):
    """
    Solves a Sudoku puzzle in-place using a backtracking algorithm.

    Args:
        board (list): A 2D list representing the Sudoku board, where each cell is a number from 0-9 or an empty string.

    Returns:
        bool: True if the puzzle was successfully solved, False otherwise.
    """

    def is_valid(board, row, col, num):
        """
        Checks whether it's possible to place a number in a given position on the board.

        Args:
            board (list): A 2D list representing the Sudoku board.
            row (int): The current row index.
            col (int): The current column index.
            num (int): The number to be placed in the cell at (row, col).

        Returns:
            bool: True if it's possible to place the number, False otherwise.
        """
        for x in range(9):
            if board[row][x] == num and x != col:
                return False
        for x in range(9):
            if board[x][col] == num and x != row:
                return False
        start_row = row - row % 3
        start_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if board[i + start_row][j + start_col] == num and (i + start_row != row or j + start_col != col):
                    return False
        return True

    def solve(board):
        """
        Recursively attempts to fill the Sudoku board with valid numbers.

        Args:
            board (list): A 2D list representing the Sudoku board.
        """
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    for num in range(1, 10):
                        if is_valid(board, i, j, num):
                            board[i][j] = num
                            if solve(board):
                                return True
                            board[i][j] = 0
                    return False
        return True
    solve(board)