def count_islands(grid):
    """
    Counts connected groups of land cells in a grid.

    Args:
        grid (list[list[str]]): A 2D list representing the grid.
            "1" represents land and "0" represents water.

    Returns:
        int: The number of connected islands.
    """
    if not grid or not all(grid):
        return 0
    rows, cols = (len(grid), len(grid[0]))
    island_count = 0

    def dfs(r, c):
        """
        Performs a Depth-First Search from the given cell.

        Args:
            r (int): The row index of the cell.
            c (int): The column index of the cell.
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
                island_count += 1
                dfs(r, c)
    return island_count