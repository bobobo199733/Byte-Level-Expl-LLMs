def sudoku_solver(board):
    def valid_number(row, col, num):
        for i in range(9):
            if board[row][i] == num or board[i][col] == num:
                return False
        box_x = row - row % 3
        box_y = col - col % 3
        for i in range(box_x, box_x + 3):
            for j in range(box_y, box_y + 3):
                if board[i][j] == num:
                    return False
        return True

    def solve_sudoku(row=0):
        if row == 9:
            return True

        for col in range(9):
            if board[row][col] != 0 and valid_number(row, col, board[row][col]):
                continue

            if board[row][col] == 0 or solve_sudoku(row + 1):
                board[row][col] = board[row][col] if board[row][col] != 0 else row+1
                if row == 8:
                    return True
                continue

            board[row][col] = 0

        else:
            return False

    if any(row with 0 > max(row) for row in board) or any(0 < min(row) for row in board):
        raise ValueError("Invalid puzzle")

    solve_sudoku()