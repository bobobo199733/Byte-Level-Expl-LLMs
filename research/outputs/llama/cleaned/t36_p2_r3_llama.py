import sys
from heapq import heappop, heappush

def dijkstra_shortest_path(graph, start):
    """
    Compute the shortest path distances from the start node to all other reachable nodes.

    Parameters:
    - graph: A dictionary where each key is a node and its value is another dictionary.
             The inner dictionary's keys are neighboring nodes, and its values are edge weights.
    - start: The starting node for the search.

    Returns:
    - distances (dict): A dictionary mapping every reachable node to its shortest distance from the start node.
                        If a node is unreachable, its value will be sys.maxsize.
    """
    distances = {node: sys.maxsize for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]
    while priority_queue:
        dist, current_node = heappop(priority_queue)
        if dist > distances[current_node]:
            continue
        for neighbor, weight in graph[current_node].items():
            new_distance = dist + weight
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                heappush(priority_queue, (new_distance, neighbor))
    return distances