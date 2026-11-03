def count_islands(grid):
    if not grid:
        return 0
    rows, cols = (len(grid), len(grid[0]))
    visit = set()

    def dfs(r, c):
        if r < 0 or r == rows or c < 0 or (c == cols) or (grid[r][c] == '0') or ((r, c) in visit):
            return
        visit.add((r, c))
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 'L' and (r, c) not in visit:
                count += 1
                dfs(r, c)
    return count