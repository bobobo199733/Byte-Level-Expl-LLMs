def sudoku_solver(board):

    def is_valid(r, c, val):
        for i in range(9):
            if board[r][i] == val:
                return False
        for i in range(9):
            if board[i][c] == val:
                return False
        box_x = r - r % 3
        box_y = c - c % 3
        for i in range(box_x, box_x + 3):
            for j in range(box_y, box_y + 3):
                if board[i][j] == val:
                    return False
        return True

    def solve_sudoku(r, c):
        if r == 9 and c == 9:
            return True
        for i in range(1, 10):
            val = board[r][c]
            if val != 0:
                continue
            if not is_valid(r, c, i):
                continue
            board[r][c] = i
            if solve_sudoku(r + 1, c):
                return True
            board[r][c] = val
        if r < 8:
            for i in range(1, 10):
                if board[r + 1][c] == 0:
                    break
            if i == 10:
                return False
        if r == 8 and c == 8 and (not board[r][c]):
            raise ValueError('Unsolvable Sudoku puzzle')
        return False
    solve_sudoku(0, 0)