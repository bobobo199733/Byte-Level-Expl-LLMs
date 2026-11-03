def sudoku_solver(board):

    def is_valid(row, col, num):
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

    def solve_sudoku(board):
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    for num in range(1, 10):
                        if is_valid(row, col, num):
                            board[row][col] = num
                            if solve_sudoku(board):
                                return True
                            board[row][col] = 0
                    return False
        return True
    if not isinstance(board, list) or len(board) != 81:
        raise ValueError('Invalid puzzle.')
    for row in board:
        if not all((isinstance(num, int) and 0 <= num < 10 for num in row)):
            raise ValueError('Invalid puzzle.')
    solve_sudoku(board)
    return board