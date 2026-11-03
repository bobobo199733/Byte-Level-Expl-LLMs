def sudoku_solver(board):

    def find_empty(board):
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] == 0:
                    return (i, j)
        return None

    def is_valid(row, col, num, board):
        for i in range(len(board)):
            if board[i][col] == num and i != row:
                return False
        for j in range(len(board)):
            if board[row][j] == num and j != col:
                return False
        box_x = row - row % 3
        box_y = col - col % 3
        for i in range(box_x, box_x + 3):
            for j in range(box_y, box_y + 3):
                if board[i][j] == num and (i != row or j != col):
                    return False
        return True

    def sudoku_helper(board, row=0, col=0):
        if row == len(board):
            return True
        if col == len(board[row]):
            return sudoku_helper(board, row + 1, 0)
        if board[row][col] != 0:
            return sudoku_helper(board, row, col + 1)
        for num in range(1, len(board[row]) + 1):
            if is_valid(row, col, num, board):
                board[row][col] = num
                if sudoku_helper(board, row, col + 1):
                    return True
        board[row][col] = 0
        return False
    if not sudoku_helper(board):
        print('No solution found.')
        return None
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 0:
                print('Unsolved cell: ', (i, j))
    return board