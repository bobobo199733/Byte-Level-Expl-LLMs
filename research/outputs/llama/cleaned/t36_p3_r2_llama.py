def dijkstra_shortest_path(graph, start):
    """
    Compute the shortest path from the given `start` node to all other nodes in the weighted graph.

    Args:
        graph (dict): Adjacency list representation of the graph.
            Each key is a node, and its corresponding value is another dictionary.
            The inner dictionary has neighboring nodes as keys and edge weights as values.
        start (str or int): Node ID where to begin searching for shortest paths.

    Returns:
        dict: Dictionary with shortest distances from `start` to all other nodes.
        Each key is a node, and its corresponding value is the minimum distance.
    """
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]
    while priority_queue:
        current_distance, current_node = min(priority_queue)
        priority_queue.remove((current_distance, current_node))
        if current_distance > distances[current_node]:
            continue
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                priority_queue.append((distance, neighbor))
    return distances