from collections import deque

def bfs_shortest_path(graph, start, target):
    """
    Compute the shortest distance between two nodes in an unweighted graph using breadth-first search.

    Args:
        graph (dict): Adjacency list representation of the graph.
        start (node): Starting node.
        target (node): Target node.

    Returns:
        int: Shortest distance between start and target nodes. Returns -1 if no path exists.
    """
    if start not in graph or target not in graph:
        return -1
    queue = deque([(start, 0)])
    visited = {start}
    while queue:
        node, distance = queue.popleft()
        if node == target:
            return distance
        for neighbor in graph[node]:
            if neighbor not in visited:
                queue.append((neighbor, distance + 1))
                visited.add(neighbor)
    return -1