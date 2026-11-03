def count_islands(grid):

    def dfs(x, y):
        if x < 0 or y < 0 or x >= len(grid) or (y >= len(grid[0])) or (grid[x][y] == '0'):
            return
        grid[x][y] = '0'
        dfs(x + 1, y)
        dfs(x - 1, y)
        dfs(x, y + 1)
        dfs(x, y - 1)
    count = 0
    for row in grid:
        for _ in row if row else ():
            if row[_] == '1':
                dfs(row.index(_), _)
                count += 1
    return count