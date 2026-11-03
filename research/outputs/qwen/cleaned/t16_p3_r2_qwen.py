def sudoku_solver(board):

    def is_valid(num, row, col):
        for i in range(9):
            if board[row][i] == num:
                return False
        for i in range(9):
            if board[i][col] == num:
                return False
        box_row = row // 3 * 3
        box_col = col // 3 * 3
        for i in range(3):
            for j in range(3):
                if board[box_row + i][box_col + j] == num:
                    return False
        return True

    def solve():
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if is_valid(num, row, col):
                            board[row][col] = num
                            if solve():
                                return True
                            else:
                                board[row][col] = 0
                    return False
        return True
    if solve():
        return board
    else:
        print('No solution exists.')
        return None