def count_islands(grid):
    """
    Counts the number of islands in a 2D grid.

    Args:
        grid (list[list[int]]): A 2D grid where 1 represents land and 0 represents water.

    Returns:
        int: The number of islands in the grid.
    """
    if not grid:
        return 0
    rows, cols = (len(grid), len(grid[0]))
    island_count = 0

    def dfs(row, col):
        """
        Performs a depth-first search from the given cell.

        Args:
            row (int): The row index of the cell.
            col (int): The column index of the cell.
        """
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