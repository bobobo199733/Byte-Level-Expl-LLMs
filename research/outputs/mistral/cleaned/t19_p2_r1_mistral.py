def count_islands(grid):
    if not grid:
        return 0
    rows = len(grid)
    cols = len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    island_count = 0

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or (c >= cols) or visited[r][c]:
            return
        visited[r][c] = True
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)
    for r in range(rows):
        for c in range(cols):
            if not visited[r][c] and grid[r][c] == '1':
                island_count += 1
                dfs(r, c)
    return island_count