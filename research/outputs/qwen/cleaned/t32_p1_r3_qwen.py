def n_queens(n):

    def solve_n_queens(board, row):
        if row == n:
            return [board.copy()]
        solutions = []
        for col in range(n):
            if is_safe(board, row, col):
                board[row] = col
                solutions.extend(solve_n_queens(board, row + 1))
        return solutions

    def is_safe(board, row, col):
        for i in range(row):
            if board[i] == col or board[i] - i == col - row or board[i] + i == col + row:
                return False
        return True
    initial_board = [None] * n
    solutions = solve_n_queens(initial_board, 0)
    result = []
    for solution in solutions:
        result.append([[i, col] for i, col in enumerate(solution)])
    return result