def n_queens(n):
    """
    Returns all valid solutions for the N-Queens problem where no queens attack each other.
    
    Args:
        n (int): The number of queens to place on an n x n chessboard.
    
    Returns:
        list: A list of lists, where each sublist represents a row of queens in a solution.
              Each queen is represented by her column index (0-based).
    """
    if n <= 1:
        return [[]]

    def solve(queens, xy_dif, xy_sum):
        if len(queens) == n:
            return [queens[:]]
        solutions = []
        for i in range(n):
            if i in queens or xy_dif + i in xy_dif or xy_sum - i in xy_sum:
                continue
            solve(queens + [i], xy_dif + {i}, xy_sum | {n + i})
        return solutions
    return solve([], set(), set())