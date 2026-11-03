def n_queens(n):

    def place_queen(queens, i):
        for j in range(len(queens)):
            if queens[j] == i or abs(queens[j] - i) == abs(j - len(queens)):
                return False
        queens.append(i)
        if len(queens) == n:
            yield queens[:]
        for k in range(i + 1, len(board)):
            if place_queen(queens, k):
                yield from place_queens([], i + 1)
    board = list(range(n))
    yield from place_queens([], 0)