def n_queens(n):

    def is_safe(board, row, col):
        for i in range(col):
            if board[row][i] == 1:
                return False
        for i, j in zip(range(row, -1, -1), range(col, -1, -1)):
            if board[i][j] == 1:
                return False
        for i, j in zip(range(row, n, 1), range(col, -1, -1)):
            if board[i][j] == 1:
                return False
        return True

    def solve_n_queens_util(board, col):
        if col >= n:
            result = []
            for i in range(n):
                temp_row = []
                for j in range(n):
                    temp_row.append('.' if board[i][j] == 0 else 'Q')
                result.append(''.join(temp_row))
            solutions.append(result)
            return True
        res = False
        for i in range(n):
            if is_safe(board, i, col):
                board[i][col] = 1
                res = solve_n_queens_util(board, col + 1) or res
                board[i][col] = 0
        return res
    solutions = []
    initial_board = [[0 for _ in range(n)] for _ in range(n)]
    solve_n_queens_util(initial_board, 0)
    return solutions