def bfs_shortest_path(graph, start, target):
    """
    Compute the shortest distance between two nodes using BFS.
    
    :param graph: A dictionary representing an unweighted graph where keys are node labels and values are lists of adjacent nodes.
    :param start: The starting node label.
    :param target: The target node label.
    :return: The length of the shortest path if one exists, otherwise -1.
    """
    if start not in graph or target not in graph:
        return -1
    queue = [(start, 0)]
    visited = {start: True}
    while queue:
        current_node, distance = queue.pop(0)
        if current_node == target:
            return distance
        for neighbor in graph[current_node]:
            if neighbor not in visited:
                visited[neighbor] = True
                queue.append((neighbor, distance + 1))
    return -1