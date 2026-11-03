from collections import deque

def count_islands(grid):
    if not grid:
        return 0
    rows, cols = (len(grid), len(grid[0]))
    directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]

    def bfs(r, c):
        queue = deque([(r, c)])
        while queue:
            row, col = queue.popleft()
            for dr, dc in directions:
                new_r, new_c = (row + dr, col + dc)
                if 0 <= new_r < rows and 0 <= new_c < cols and (grid[new_r][new_c] == '1'):
                    grid[new_r][new_c] = '0'
                    queue.append((new_r, new_c))
    island_count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                bfs(r, c)
                island_count += 1
    return island_count