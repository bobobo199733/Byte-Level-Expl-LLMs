from collections import defaultdict
import sys

def bfs_shortest_path(graph, start, target):
    if start not in graph or target not in graph:
        raise ValueError('Both start and target nodes must be present in the graph.')
    visited = {node: False for node in graph}
    distances = {node: sys.maxsize for node in graph}
    distances[start] = 0
    queue = [(start, 0)]
    while queue:
        current_node, current_distance = queue.pop(0)
        if visited[current_node]:
            continue
        visited[current_node] = True
        for neighbor, edge_weight in graph[current_node].items():
            new_distance = current_distance + edge_weight
            if neighbor not in visited or new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                queue.append((neighbor, new_distance))
    return distances[target] if target in distances else -1