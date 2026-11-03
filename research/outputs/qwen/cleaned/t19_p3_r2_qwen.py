def count_islands(grid):
    if not grid or not grid[0]:
        return 0
    rows, cols = (len(grid), len(grid[0]))
    visited = set()

    def dfs(r, c):
        if r < 0 or c < 0 or r >= rows or (c >= cols) or ((r, c) in visited) or (grid[r][c] == '0'):
            return
        visited.add((r, c))
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)
    island_count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1' and (r, c) not in visited:
                dfs(r, c)
                island_count += 1
    return island_count