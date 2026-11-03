def dijkstra_shortest_path(graph, start):
    """
    Compute the shortest distance from the start node to all reachable nodes using Dijkstra's algorithm.

    Args:
        graph (dict): Adjacency list representation of the graph, where each key is a node and its value is another dictionary.
                     The inner dictionary has neighboring nodes as keys and edge weights as values.
        start (node): Starting node for the shortest path computation.

    Returns:
        dict: A dictionary with all reachable nodes as keys and their corresponding shortest distances from the start node as values.
    """
    distances = {node: float('inf') if node != start else 0 for node in graph}
    unvisited_nodes = set(graph.keys())
    while unvisited_nodes:
        current_node = min(unvisited_nodes, key=lambda node: distances[node])
        unvisited_nodes.remove(current_node)
        for neighbor, weight in graph[current_node].items():
            tentative_distance = distances[current_node] + weight
            if tentative_distance < distances[neighbor]:
                distances[neighbor] = tentative_distance
    return distances