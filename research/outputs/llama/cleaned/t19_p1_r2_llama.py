def count_islands(grid):
    """
    Counts the number of islands in a 2D grid.

    Args:
        grid (list[list[int]]): A 2D grid represented as a list of lists, where each element is either 0 or 1.
            0 represents water and 1 represents land.

    Returns:
        int: The number of islands in the grid.

    Example:
        >>> grid = [
        ...     [1, 1, 1, 1, 0],
        ...     [1, 1, 0, 1, 0],
        ...     [1, 1, 0, 0, 0],
        ...     [0, 0, 0, 0, 0]
        ... ]
        >>> count_islands(grid)
        1
    """
    if not grid:
        return 0
    rows, cols = (len(grid), len(grid[0]))
    island_count = 0

    def dfs(row, col):
        """Performs DFS from the given position."""
        if row < 0 or row >= rows or col < 0 or (col >= cols) or (grid[row][col] == 0):
            return
        grid[row][col] = 0
        dfs(row - 1, col)
        dfs(row + 1, col)
        dfs(row, col - 1)
        dfs(row, col + 1)
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == 1:
                island_count += 1
                dfs(row, col)
    return island_count