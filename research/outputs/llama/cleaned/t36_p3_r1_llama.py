def dijkstra_shortest_path(graph, start):
    """
    Computes the shortest path from the start node to all other nodes in the graph.

    Args:
        graph (dict): A dictionary representing the graph, where each key is a node
            and its corresponding value is another dictionary with neighboring nodes
            as keys and edge weights as values.
        start (str): The node from which to start the search.

    Returns:
        dict: A dictionary where each key is a node in the graph and its corresponding
            value is the shortest distance from the start node to that node. If a node
            is unreachable, its value will be None.
    """
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous_nodes = {}
    unvisited_nodes = set(graph.keys())
    while unvisited_nodes:
        current_node = min(unvisited_nodes, key=lambda x: distances[x])
        unvisited_nodes.remove(current_node)
        if distances[current_node] == float('inf'):
            break
        for neighbor, weight in graph[current_node].items():
            distance = distances[current_node] + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
    return (distances, previous_nodes)