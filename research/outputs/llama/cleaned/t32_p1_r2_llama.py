def n_queens(n):
    """
    Returns all valid board configurations for the N-Queens problem.

    Args:
        n (int): The number of queens on the board.

    Returns:
        list: A list of lists, where each sublist represents a solution.
              Each element in the sublist is an index of a queen's position.
    """

    def backtrack(queens, empty_cols):
        if len(empty_cols) == 0:
            solutions.append(queens[:])
            return
        for col in empty_cols:
            queens.append(col)
            new_empty_cols = empty_cols[:]
            new_empty_cols.remove(col)
            backtrack(queens, new_empty_cols)
            queens.pop()
    solutions = []
    backtrack([], list(range(n)))
    return [['.' * i + 'Q' + '.' * (n - 1 - i) for i in sol] for sol in solutions]