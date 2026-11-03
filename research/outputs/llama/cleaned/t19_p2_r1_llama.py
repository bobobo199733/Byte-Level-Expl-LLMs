def count_islands(grid):
    """
    Counts connected groups of land cells in a grid.

    :param grid: A 2D list of strings where "1" represents land and "0" represents water.
    :return: The number of islands (connected groups of land) in the grid.
    """
    if not grid:
        return 0
    rows, cols = (len(grid), len(grid[0]))
    visited = [[False] * cols for _ in range(rows)]

    def dfs(r, c):
        """Performs DFS from a given cell."""
        if r < 0 or r >= rows or c < 0 or (c >= cols) or (grid[r][c] == '0') or visited[r][c]:
            return
        visited[r][c] = True
        dfs(r - 1, c)
        dfs(r + 1, c)
        dfs(r, c - 1)
        dfs(r, c + 1)
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1' and (not visited[r][c]):
                dfs(r, c)
                count += 1
    return count