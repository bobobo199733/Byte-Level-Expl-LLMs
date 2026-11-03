from collections import deque

def bfs_shortest_path(graph, start, target):
    """
    Returns the length of the shortest path between 'start' and 'target' in the graph.

    Args:
        graph (dict): Adjacency list representation of the graph.
        start (str): Node to start searching from.
        target (str): Target node.

    Returns:
        int: Length of the shortest path, or -1 if no path exists.
    """
    if start not in graph or target not in graph:
        raise ValueError('Start or target node is not in the graph')
    queue = deque([(start, 0)])
    visited = {start}
    while queue:
        node, dist = queue.popleft()
        if node == target:
            return dist
        for neighbor in graph[node]:
            if neighbor not in visited:
                queue.append((neighbor, dist + 1))
                visited.add(neighbor)
    return -1