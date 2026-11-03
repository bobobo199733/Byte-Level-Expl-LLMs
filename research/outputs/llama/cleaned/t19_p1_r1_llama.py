def count_islands(grid):
    """
    Counts the number of islands in a 2D grid.

    Args:
        grid (list[list[int]]): A 2D list representing the grid, where 1 indicates land and 0 indicates water.

    Returns:
        int: The total number of islands.
    """
    if not grid:
        return 0
    rows, cols = (len(grid), len(grid[0]))
    count = 0

    def dfs(r, c):
        """
        Performs a depth-first search from the given cell (r, c).

        Args:
            r (int): The row index.
            c (int): The column index.
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
                count += 1
                dfs(r, c)
    return count