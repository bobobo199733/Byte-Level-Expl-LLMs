def sudoku_solver(board):
    """
    Solves a standard 9x9 Sudoku puzzle in-place.

    Args:
        board (list of lists): A 2D list representing the Sudoku board.
            Empty cells are represented by 0.

    Raises:
        ValueError: If the puzzle is invalid or unsolvable.
    """

    def is_valid(board, row, col, num):
        """
        Checks if a number can be placed in a given position on the board.

        Args:
            board (list of lists): The Sudoku board.
            row (int): The row index of the position.
            col (int): The column index of the position.
            num (int): The number to check.

        Returns:
            bool: True if the number can be placed, False otherwise.
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

    def solve_sudoku(board):
        """
        Solves the Sudoku puzzle using backtracking.

        Args:
            board (list of lists): The Sudoku board.
        """
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    for num in range(1, 10):
                        if is_valid(board, i, j, num):
                            board[i][j] = num
                            solve_sudoku(board)
                            board[i][j] = 0
                    raise ValueError('Puzzle is unsolvable')
        return True
    try:
        solve_sudoku(board)
    except ValueError as e:
        raise ValueError(f'Error: {e}')