def n_queens(n):
    """
    Returns all valid N-Queens solutions.

    :param n: The size of the chessboard (number of rows and columns).
    :return: A list of lists, where each inner list represents a solution.
             Each solution is represented as a list of column indices for each row.
    """

    def solve(queens):
        if len(queens) == n:
            return [queens[:]]
        result = []
        for col in range(n):
            if all((abs(col - q[0]) != abs(i - len(q)) and i < len(q) for i, q in enumerate(queens))):
                new_queens = queens + [col]
                result.extend(solve(new_queens))
        return result
    return solve([0])