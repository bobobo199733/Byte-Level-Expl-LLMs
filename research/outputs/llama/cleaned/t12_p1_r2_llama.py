from collections import deque

def bfs_shortest_path(graph, start, target):
    """
    Calculate the length of the shortest path between two nodes in an unweighted graph.

    Args:
        graph (dict): Adjacency list representation of the graph.
        start (node): Starting node for the search.
        target (node): Target node to find the shortest path to.

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