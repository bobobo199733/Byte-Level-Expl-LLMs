import sys

def dijkstra_shortest_path(graph, start):
    """
    Compute the shortest distances from a start node to all other reachable nodes in a weighted graph.

    Args:
        graph (dict): A dictionary representing the adjacency list of the graph.
            Each key is a node and its corresponding value is another dictionary with neighboring nodes as keys
            and edge weights as values.
        start (node): The node from which to compute shortest distances.

    Returns:
        dict: A dictionary containing the shortest distance from the start node to every reachable node.
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