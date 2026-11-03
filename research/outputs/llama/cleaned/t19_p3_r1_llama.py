def count_islands(grid):
    """
    Counts the number of islands in a given 2D grid.

    Args:
        grid (list): A 2D list representing the grid, where each cell contains either '0' or '1'.

    Returns:
        int: The total number of islands.
    """
    if not isinstance(grid, list) or not all((isinstance(row, list) for row in grid)):
        raise ValueError('Invalid input. Grid must be a 2D list.')

    def dfs(row, col):
        """
        Helper function to perform DFS on a given cell.

        Args:
            row (int): The current row index.
            col (int): The current column index.
        """
        if 0 <= row < len(grid) and 0 <= col < len(grid[0]) and (grid[row][col] == '1'):
            grid[row][col] = '0'
            dfs(row - 1, col)
            dfs(row + 1, col)
            dfs(row, col - 1)
            dfs(row, col + 1)
    island_count = 0
    for row_idx, row in enumerate(grid):
        for col_idx, _ in enumerate(row):
            if grid[row_idx][col_idx] == '1':
                dfs(row_idx, col_idx)
                island_count += 1
    return island_count