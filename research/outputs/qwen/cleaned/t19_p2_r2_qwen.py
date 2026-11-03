def count_islands(grid):
    if not grid:
        return 0

    def dfs(x, y):
        if x < 0 or x >= len(grid) or y < 0 or (y >= len(grid[0])) or (grid[x][y] == '0'):
            return
        grid[x][y] = '0'
        dfs(x + 1, y)
        dfs(x - 1, y)
        dfs(x, y + 1)
        dfs(x, y - 1)
    count = 0
    rows, cols = (len(grid), len(grid[0]))
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == '1':
                dfs(i, j)
                count += 1
    return count