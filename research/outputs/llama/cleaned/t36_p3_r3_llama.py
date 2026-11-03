def dijkstra_shortest_path(graph, start):
    """
    Compute the shortest paths from `start` node to all other nodes in the graph.

    :param graph: A dictionary representing the graph where each key is a node and its value is another dictionary.
                  The inner dictionary's keys are neighboring nodes and values are edge weights.
    :type graph: dict
    :param start: The node from which to compute shortest paths.
    :type start: str
    :return: A dictionary where the keys are destination nodes and the values are dictionaries with 'distance' and 'previous_node' attributes.
             These attributes represent the minimum distance and previous node in the shortest path, respectively.
    :rtype: dict
    """
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    unvisited_nodes = list(graph.keys())
    while unvisited_nodes:
        current_node = min(unvisited_nodes, key=lambda node: distances[node])
        unvisited_nodes.remove(current_node)
        for neighbor, weight in graph[current_node].items():
            distance = distances[current_node] + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                graph[neighbor]['previous_node'] = current_node
    for node in graph:
        if node != start and (not hasattr(graph[node], 'previous_node')):
            del graph[node]['previous_node']
    return distances