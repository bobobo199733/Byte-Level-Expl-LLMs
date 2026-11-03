def sudoku_solver(board):
    """
    Solves a standard 9x9 Sudoku puzzle in-place using backtracking.

    Args:
        board (list of lists): The 2D list representing the Sudoku board.
            Empty cells are represented by 0. Rows and columns are indexed from 1 to 9.
            Boxes are identified by their top-left corner cell's index.

    Raises:
        ValueError: If the puzzle is invalid or unsolvable.

    Returns:
        None
    """

    def is_valid(board, row, col, num):
        """
        Checks if a number can be placed in a given cell according to Sudoku rules.

        Args:
            board (list of lists): The 2D list representing the Sudoku board.
            row: The row index of the cell (1-9).
            col: The column index of the cell (1-9).
            num: The number to be placed in the cell (1-9).

        Returns:
            bool: True if the number can be placed, False otherwise.
        """
        if num in board[row] or num in [row[i] for i in range(9)]:
            return False
        box_row = row // 3 * 3
        box_col = col // 3 * 3
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if board[r][c] == num:
                    return False
        return True

    def solve(board):
        """
        Recursively attempts to fill the Sudoku board with numbers.

        Args:
            board (list of lists): The 2D list representing the Sudoku board.

        Raises:
            ValueError: If the puzzle is invalid or unsolvable.
        """
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if is_valid(board, row, col, num):
                            board[row][col] = num
                            if solve(board):
                                return True
                            board[row][col] = 0
                    raise ValueError('Invalid or unsolvable puzzle')
        return True
    try:
        solve(board)
    except ValueError as e:
        print(e)