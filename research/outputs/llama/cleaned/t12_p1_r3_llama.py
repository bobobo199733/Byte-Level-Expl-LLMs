from collections import deque

def bfs_shortest_path(graph, start, target):
    """
    Returns the length of the shortest path between two nodes in an unweighted graph.

    Args:
        graph (dict): Adjacency list representation of the graph.
        start (node): The starting node for the BFS traversal.
        target (node): The target node to find the shortest path from the start node.

    Returns:
        int: The length of the shortest path between the start and target nodes. If there is no path, returns -1.
    """
    if not graph or start not in graph or target not in graph:
        return -1
    queue = deque([(start, 0)])
    visited = set()
    while queue:
        current_node, distance = queue.popleft()
        if current_node == target:
            return distance
        visited.add(current_node)
        for neighbor in graph[current_node]:
            if neighbor not in visited:
                queue.append((neighbor, distance + 1))
    return -1