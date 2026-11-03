from collections import deque

def bfs_shortest_path(graph, start, target):
    """
    Returns the shortest distance between two nodes using BFS.

    Args:
        graph (dict): Adjacency list representation of the graph.
        start (node): Starting node.
        target (node): Target node.

    Returns:
        int: Shortest distance between start and target nodes. If no path exists, returns -1.
    """
    if start not in graph or target not in graph:
        raise ValueError('Start or target node is not in the graph')
    queue = deque([(start, 0)])
    visited = set()
    while queue:
        node, dist = queue.popleft()
        if node == target:
            return dist
        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                queue.append((neighbor, dist + 1))
    return -1