def n_queens(n):

    def backtrack(row):
        if row == n:
            result.append(['.' * col + 'Q' + '.' * (n - col - 1) for col in board])
            return
        for col in range(n):
            if all((not conflict[col] and (not conflict[row + i + col]) and (not conflict[n - 1 + col - i]) for i in range(n))):
                board.append(col)
                conflict[col] = True
                conflict[row + col] = True
                conflict[n - 1 + col - row] = True
                backtrack(row + 1)
                board.pop()
                conflict[col] = False
                conflict[row + col] = False
                conflict[n - 1 + col - row] = False
    if n <= 0:
        return []
    result = []
    board = []
    conflict = [False] * (2 * n)
    backtrack(0)
    return result