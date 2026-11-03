from collections import deque

def bfs_shortest_path(graph, start, target):
    """
    Returns the shortest distance between two nodes using BFS.

    Args:
        graph (dict): Adjacency list representation of the graph.
        start (str): Node to start the search from.
        target (str): Target node to find the shortest path to.

    Returns:
        int: Shortest distance between start and target nodes. If no path exists, returns -1.
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