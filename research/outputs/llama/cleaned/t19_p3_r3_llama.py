def count_islands(grid):
    """
    Counts the number of islands in a given 2D grid.

    Args:
        grid (list): A 2D list of boolean values where True represents land and False represents water.

    Returns:
        int: The total number of islands.
    """
    if not grid:
        return 0
    rows, cols = (len(grid), len(grid[0]))

    def dfs(row, col):
        """
        Performs a Depth-First Search from the given row and column.

        Args:
            row (int): The current row index.
            col (int): The current column index.
        """
        if 0 <= row < rows and 0 <= col < cols and grid[row][col]:
            grid[row][col] = False
            dfs(row - 1, col)
            dfs(row + 1, col)
            dfs(row, col - 1)
            dfs(row, col + 1)
    count = 0
    for row in range(rows):
        for col in range(cols):
            if grid[row][col]:
                dfs(row, col)
                count += 1
    return count