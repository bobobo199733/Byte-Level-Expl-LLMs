def n_queens(n):
    """
    Returns all valid N-Queens solutions.
    
    Args:
        n (int): Size of the board.
    
    Returns:
        list[list[int]]: A list of lists, where each sublist represents a solution and contains the row indices of queens in that solution.
    """

    def is_safe(board, row, col):
        """
        Checks if it's safe to place a queen at (row, col) position on the board.
        
        Args:
            board (list[int]): Current state of the board.
            row (int): Row index where we want to place a queen.
            col (int): Column index where we want to place a queen.
        
        Returns:
            bool: True if it's safe, False otherwise.
        """
        for i in range(row):
            if board[i] == col or board[i] - i == col - row or board[i] + i == col + row:
                return False
        return True

    def place_queens(board, n, row):
        """
        Places queens on the board using backtracking.
        
        Args:
            board (list[int]): Current state of the board.
            n (int): Size of the board.
            row (int): Current row we're trying to fill with queens.
        
        Returns:
            list[list[int]]: A list of lists, where each sublist represents a solution and contains the row indices of queens in that solution.
        """
        if row == n:
            solutions.append(board[:])
            return
        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                place_queens(board, n, row + 1)
    solutions = []
    place_queens([-1] * n, n, 0)
    return [[col + 1 for col in sol] for sol in solutions]