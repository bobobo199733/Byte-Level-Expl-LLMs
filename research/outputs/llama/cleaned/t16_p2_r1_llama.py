def sudoku_solver(board):
    """
    Solves a standard 9x9 Sudoku puzzle using backtracking.

    Args:
        board (list): A 2D list representing the Sudoku puzzle. Empty cells are represented by 0.
            The puzzle must be valid and solvable for this function to work.

    Raises:
        ValueError: If the input puzzle is invalid or unsolvable.

    Returns:
        None
    """

    def is_valid(board, row, col, num):
        box_size = 9 // 3
        box_row_start, box_col_start = (row - row % box_size, col - col % box_size)
        for r in range(box_row_start, box_row_start + box_size):
            for c in range(box_col_start, box_col_start + box_size):
                if board[r][c] == num:
                    return False
        if num in board[row]:
            return False
        if num in [board[r][col] for r in range(9)]:
            return False
        return True

    def fill_board(board):
        """
        Attempts to fill a cell with a valid number using backtracking.
        If no valid number can be found, it raises an exception.

        Args:
            board (list): A 2D list representing the Sudoku puzzle.

        Returns:
            bool: Whether or not all cells were filled successfully.
        """
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if is_valid(board, row, col, num):
                            board[row][col] = num
                            if fill_board(board):
                                return True
                            board[row][col] = 0
                    raise ValueError('Puzzle is unsolvable')
        return True
    try:
        fill_board(board)
    except ValueError as e:
        raise ValueError(f'Invalid or unsolvable puzzle: {e}')