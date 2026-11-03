def n_queens(n):
    """
    Returns all valid board configurations for the N-Queens problem.
    
    Parameters:
        n (int): The size of the square board.
        
    Returns:
        list[list[str]]: A list of all valid board configurations. Each configuration is represented as a list of strings, where 'Q' denotes a queen and '.' denotes an empty space.
    """

    def backtrack(row):
        if row == n:
            solution = [''.join(board[i]) for i in range(n)]
            solutions.append(solution)
            return
        for col in range(n):
            if is_valid(board, row, col):
                board[row] = board[row][:col] + 'Q' + board[row][col + 1:]
                backtrack(row + 1)

    def is_valid(board, row, col):
        for i in range(row):
            if board[i] == '.' * col or board[i][col - (row - i)] == 'Q':
                return False
        return True
    solutions = []
    board = ['.'] * n
    backtrack(0)
    return solutions