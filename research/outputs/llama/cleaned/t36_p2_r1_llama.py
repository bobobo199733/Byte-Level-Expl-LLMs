import heapq

def dijkstra_shortest_path(graph, start):
    """
    Compute shortest path distances from the `start` node to every reachable node in a weighted graph.

    Args:
        graph (dict): Adjacency list representation of the graph. Each key is a node and its value is another dictionary with neighboring nodes as keys and edge weights as values.
        start (node): The node from which to compute shortest paths.

    Returns:
        dict: A dictionary where each key is a node in the graph, and its corresponding value is the shortest distance from `start` to that node. Nodes not reachable from `start` have a distance of infinity.

    Raises:
        ValueError: If `start` is not a valid node in the graph.
    """
    if start not in graph:
        raise ValueError('Start node not found in the graph')
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    pq = [(0, start)]
    while pq:
        dist, current_node = heapq.heappop(pq)
        if dist > distances[current_node]:
            continue
        for neighbor, weight in graph[current_node].items():
            new_dist = distances[current_node] + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                heapq.heappush(pq, (new_dist, neighbor))
    return distances