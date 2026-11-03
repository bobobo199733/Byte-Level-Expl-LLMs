def count_islands(grid):
    if not grid:
        return 0
    rows = len(grid)
    cols = len(grid[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    island_count = 0

    def dfs(x, y):
        if x < 0 or x >= rows or y < 0 or (y >= cols) or (grid[x][y] == '0') or visited[x][y]:
            return
        visited[x][y] = True
        dfs(x + 1, y)
        dfs(x - 1, y)
        dfs(x, y + 1)
        dfs(x, y - 1)
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == '1' and (not visited[i][j]):
                island_count += 1
                dfs(i, j)
    return island_count