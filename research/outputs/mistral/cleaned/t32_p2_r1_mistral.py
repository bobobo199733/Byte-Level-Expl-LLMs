def n_queens(n):

    def is_safe(board, row, col):
        for i in range(row):
            if board[i] == col or abs(board[i] - col) == abs(i - row):
                return False
        return True

    def solve_n_queens(board, n, solutions=[]):
        if len(solutions) > n:
            return solutions
        for i in range(n):
            if is_safe(board, i, board[-1] + 1 if board else 0):
                board.append(i)
                solutions_tmp = solve_n_queens([x for x in board[:-1]], n - 1, solutions)
                if solutions_tmp:
                    return solutions + [list(z) for z in solutions_tmp]
                board.pop()
        return []
    return solve_n_queens([], n) if n > 0 else []