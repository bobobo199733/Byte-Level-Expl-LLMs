def count_islands(grid):
    """
    Counts the number of islands in a 2D grid.

    Args:
        grid (list[list[int]]): A 2D grid where 0s represent water and 1s represent land.

    Returns:
        int: The total number of islands.
    """
    if not grid:
        return 0
    rows, cols = (len(grid), len(grid[0]))
    island_count = 0

    def dfs(r, c):
        """
        Performs DFS from a given cell and marks all connected cells as visited.

        Args:
            r (int): The row index of the current cell.
            c (int): The column index of the current cell.
        """
        if 0 <= r < rows and 0 <= c < cols and (grid[r][c] == 1):
            grid[r][c] = 0
            dfs(r - 1, c)
            dfs(r + 1, c)
            dfs(r, c - 1)
            dfs(r, c + 1)
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                island_count += 1
                dfs(r, c)
    return island_count