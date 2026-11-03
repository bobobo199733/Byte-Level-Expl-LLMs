def count_islands(grid):
    rows = len(grid)
    cols = len(grid[0]) if rows else 0

    def dfs(i, j):
        if i < 0 or j < 0 or i >= rows or (j >= cols) or (grid[i][j] != '1'):
            return
        grid[i][j] = '#'
        dfs(i + 1, j)
        dfs(i - 1, j)
        dfs(i, j + 1)
        dfs(i, j - 1)
    count = 0
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == '1':
                dfs(i, j)
                count += 1
    return count