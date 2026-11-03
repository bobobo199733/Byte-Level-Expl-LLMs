def n_queens(n):
    """
    Returns all valid solutions for the N-Queens problem.
    
    Parameters:
    n (int): The size of the chessboard.
    
    Returns:
    list: A list of lists, where each sublist represents a solution with a queen in each position.
    """

    def is_valid(board, row, col):
        for i in range(row):
            if board[i] == col or abs(i - row) == abs(board[i] - col):
                return False
        return True

    def backtrack(board, row):
        if row == n:
            solutions.append(board[:])
            return
        for col in range(n):
            if is_valid(board, row, col):
                board[row] = col
                backtrack(board, row + 1)
    solutions = []
    if n <= 0:
        return solutions
    board = [-1] * n
    backtrack(board, 0)
    return solutions