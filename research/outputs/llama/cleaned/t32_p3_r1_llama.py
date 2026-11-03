def n_queens(n):
    """
    Returns all valid N-Queens solutions.

    Args:
        n (int): The size of the chessboard.

    Returns:
        list: A list of lists, where each inner list represents a solution.
              Each element in the inner list is the position of a queen on the board,
              with 0 being the leftmost column and n-1 being the rightmost column.
    """

    def is_safe(board, row, col):
        """
        Checks if it's safe to place a queen at (row, col).

        Args:
            board (list): The current state of the board.
            row (int): The row index of the new queen.
            col (int): The column index of the new queen.

        Returns:
            bool: True if it's safe to place a queen at (row, col), False otherwise.
        """
        for i in range(row):
            if board[i] == col or board[i] - i == col - row or board[i] + i == col + row:
                return False
        return True

    def solve(board, row):
        """
        Recursively solves the N-Queens problem.

        Args:
            board (list): The current state of the board.
            row (int): The current row index.

        Returns:
            list: A list of lists, where each inner list represents a solution.
        """
        if row == n:
            return [board[:]]
        solutions = []
        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                solutions.extend(solve(board, row + 1))
        return solutions
    return solve([-1] * n, 0)