def count_islands(grid):

    def dfs(x, y):
        if not (0 <= x < len(grid) and 0 <= y < len(grid[0])):
            return False
        if grid[x][y] == '0':
            return False
        grid[x][y] = '0'
        count = 1
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            count += dfs(x + dx, y + dy)
        return count
    total_islands = 0
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == '1':
                total_islands += dfs(i, j)
    return total_islands