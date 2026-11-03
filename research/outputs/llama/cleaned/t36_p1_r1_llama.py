def dijkstra_shortest_path(graph, start):
    """
    Compute shortest path distances from a starting node in a weighted graph.

    Args:
        graph (dict): Adjacency list representation of the graph.
            Each key is a node and its corresponding value is another dictionary.
            The inner dictionary's keys are neighboring nodes and its values
            are the edge weights.
        start (str): Node to start the search from.

    Returns:
        dict: Shortest distance from the start node to all reachable nodes.
    """
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    unvisited_nodes = set(graph.keys())
    while unvisited_nodes:
        current_node = min(unvisited_nodes, key=lambda node: distances[node])
        unvisited_nodes.remove(current_node)
        for neighbor, weight in graph[current_node].items():
            new_distance = distances[current_node] + weight
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
    return distances