def count_islands(grid):
    if not grid:
        return 0
    rows = len(grid)
    cols = len(grid[0])
    islands_count = 0

    def dfs(row, col):
        if row < 0 or col < 0 or row >= rows or (col >= cols) or (grid[row][col] != '1'):
            return
        grid[row][col] = '0'
        dfs(row + 1, col)
        dfs(row - 1, col)
        dfs(row, col + 1)
        dfs(row, col - 1)
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == '1':
                islands_count += 1
                dfs(i, j)
    return islands_count