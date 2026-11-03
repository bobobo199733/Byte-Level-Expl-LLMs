def is_safe(board, row, col):
    for i in range(row):
        if board[i][col] == 1:
            return False
    for j in range(row + 1, min(len(board), row - col + len(board))):
        if abs(row - j) == abs(col - board[j][0]):
            return False
    return True

def n_queens(n, solution=None):
    if not solution:
        solution = []
    if len(solution) == n:
        result.append(tuple(solution))
        return solution
    for i in range(n):
        if is_safe(solution, i):
            solution.append(i)
            n_queens(n, solution)
            solution.pop()
    return solution