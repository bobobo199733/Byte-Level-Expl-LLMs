def bfs_shortest_path(graph, start, target):
    """
    Computes the shortest distance between two nodes in an unweighted graph using BFS.
    
    :param graph: A dictionary representing the adjacency list of the graph.
    :param start: The starting node for the search.
    :param target: The target node to find the path to.
    :return: The shortest distance from 'start' to 'target', or -1 if no path exists.
    """
    queue = [(start, 0)]
    visited = set()
    while queue:
        current_node, distance = queue.pop(0)
        if current_node == target:
            return distance
        if current_node not in visited:
            visited.add(current_node)
            for neighbor in graph.get(current_node, []):
                if neighbor not in visited:
                    queue.append((neighbor, distance + 1))
    return -1