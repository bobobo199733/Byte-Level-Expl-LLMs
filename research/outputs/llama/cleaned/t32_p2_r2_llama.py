def n_queens(n):
    """
    Returns all valid solutions where no queens attack each other.
    
    Args:
        n (int): The size of the chessboard.
    
    Returns:
        list: A list of lists, where each sublist represents a row on the board,
              with 1 indicating a queen and 0 indicating an empty space.
    """

    def is_valid(board, row, col):
        """
        Checks if a queen can be placed at position (row, col) without being attacked.
        
        Args:
            board (list): The current state of the board.
            row (int): The row index to check.
            col (int): The column index to check.
        
        Returns:
            bool: True if the position is valid, False otherwise.
        """
        for i in range(row):
            if board[i][col] == 1:
                return False
            if abs(board[i] - board[row]) == abs(col - i):
                return False
        return True

    def backtrack(board, row):
        """
        Recursive function to fill the board with queens.
        
        Args:
            board (list): The current state of the board.
            row (int): The current row index.
        """
        if row == n:
            result.append(board[:])
            return
        for col in range(n):
            if is_valid(board, row, col):
                board[row][col] = 1
                backtrack(board, row + 1)
                board[row][col] = 0
    result = []
    if n <= 0:
        return result
    elif n == 1:
        return [[1]]
    board = [[0] * n for _ in range(n)]
    backtrack(board, 0)
    return result