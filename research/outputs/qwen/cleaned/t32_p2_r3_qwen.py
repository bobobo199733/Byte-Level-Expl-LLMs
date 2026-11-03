def n_queens(n):

    def place_queen(row, columns, diffs, sums):
        if row == n:
            result.append(columns)
            return
        for col in range(n):
            diff = row - col
            sum_ = row + col
            if col not in columns and diff not in diffs and (sum_ not in sums):
                place_queen(row + 1, columns | {col}, diffs | {diff}, sums | {sum_})
    result = []
    place_queen(0, set(), set(), set())
    return result