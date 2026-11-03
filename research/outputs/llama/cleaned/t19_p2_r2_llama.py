def count_islands(grid):
    """
    Counts connected groups of land cells in a grid.

    Args:
        grid: A 2D list containing "1" for land and "0" for water.

    Returns:
        An integer representing the total number of islands.
    """
    if not grid or not grid[0]:
        return 0
    rows, cols = (len(grid), len(grid[0]))
    count = 0

    def dfs(r, c):
        """
        Performs DFS from a given cell.

        Args:
            r: The row index of the current cell.
            c: The column index of the current cell.
        """
        if 0 <= r < rows and 0 <= c < cols and (grid[r][c] == '1'):
            grid[r][c] = '0'
            dfs(r - 1, c)
            dfs(r + 1, c)
            dfs(r, c - 1)
            dfs(r, c + 1)
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                dfs(r, c)
                count += 1
    return count