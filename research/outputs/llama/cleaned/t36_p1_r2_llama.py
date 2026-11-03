def dijkstra_shortest_path(graph, start):
    """
    Compute shortest path distances from a starting node using Dijkstra's algorithm.

    Args:
        graph (dict): Adjacency list representation of the graph.
        start (node): Starting node.

    Returns:
        dict: Shortest distances to all reachable nodes from the start node.
    """
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    unvisited_nodes = set(graph.keys())
    while unvisited_nodes:
        current_node = min(unvisited_nodes, key=lambda x: distances[x])
        unvisited_nodes.remove(current_node)
        for neighbor, weight in graph[current_node].items():
            distance = distances[current_node] + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
    return distances