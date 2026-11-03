from collections import defaultdict
import heapq

def bfs_shortest_path(graph, start, target):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    queue = [(0, start)]
    visited = set()
    while queue:
        current_distance, current_node = heapq.heappop(queue)
        if current_node in visited:
            continue
        visited.add(current_node)
        for neighbor, edge_weight in graph[current_node].items():
            distance = current_distance + edge_weight
            if neighbor not in visited or distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))
    if distances.get(target) is not None:
        return distances[target]
    else:
        return None