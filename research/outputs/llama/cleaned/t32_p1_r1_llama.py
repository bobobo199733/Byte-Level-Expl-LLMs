def n_queens(n):
    """
    Returns all valid board configurations for the N-Queens problem.
    
    Args:
        n (int): The size of the chessboard.
    
    Returns:
        list: A list of lists, where each inner list represents a solution and contains the row indices of the queens on that board configuration.
    """

    def is_safe(board, row, col):
        """
        Checks if it's safe to place a queen at position (row, col) on the current board configuration.
        
        Args:
            board (list): The current board configuration.
            row (int): The row index of the potential new queen.
            col (int): The column index of the potential new queen.
        
        Returns:
            bool: True if it's safe to place a queen at position (row, col), False otherwise.
        """
        for i in range(row):
            if board[i] == col or board[i] - i == col - row or board[i] + i == col + row:
                return False
        return True

    def solve(board, row):
        """
        Recursively tries to fill the current row with queens.
        
        Args:
            board (list): The current board configuration.
            row (int): The current row index.
        
        Returns:
            list: A list of lists, where each inner list represents a solution and contains the row indices of the queens on that board configuration.
        """
        if row == n:
            solutions.append(board[:])
            return
        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                solve(board, row + 1)
    solutions = []
    solve([-1] * n, 0)
    return [[i + 1 for i in sol] for sol in solutions]