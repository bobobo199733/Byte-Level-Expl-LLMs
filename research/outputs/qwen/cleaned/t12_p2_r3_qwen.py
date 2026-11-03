def bfs_shortest_path(graph, start, target):
    """
    Computes the shortest path between two nodes in an unweighted graph using BFS.
    
    :param graph: A dictionary representing the graph where keys are node names and values are lists of adjacent nodes.
    :param start: The starting node for the search.
    :param target: The target node to find the shortest distance to.
    :return: The shortest distance as an integer, or -1 if no path exists.
    """
    if not graph:
        return -1
    from collections import deque
    queue = deque()
    visited = {}
    queue.append((start, 0))
    visited[start] = True
    while queue:
        current_node, distance = queue.popleft()
        if current_node == target:
            return distance
        for neighbor in graph.get(current_node, []):
            if not visited.get(neighbor, False):
                queue.append((neighbor, distance + 1))
                visited[neighbor] = True
    return -1