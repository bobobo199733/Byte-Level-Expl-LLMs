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
            solution = []
            for i in range(n):
                temp = ''
                for j in range(n):
                    temp += 'Q' if board[i][j] == 1 else '.'
                solution.append(temp)
            solutions.append(solution)
            return True
        res = False
        for i in range(n):
            if is_safe(board, i, col):
                board[i][col] = 1
                res = solve_n_queens_util(board, col + 1) or res
                board[i][col] = 0
        return res

    def print_solutions(solutions):
        for sol in solutions:
            for row in sol:
                print(row)
            print()
    board = [[0 for _ in range(n)] for _ in range(n)]
    solutions = []
    if solve_n_queens_util(board, 0):
        print_solutions(solutions)
    else:
        print('No solution exists')