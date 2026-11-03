from collections import defaultdict

def bfs_shortest_path(graph, start, target):
    visited = set()
    queue = [(start, 0)]
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    while queue:
        current_node, distance = queue.pop(0)
        visited.add(current_node)
        if current_node == target:
            return distance
        for neighbor in graph[current_node]:
            if neighbor not in visited:
                distances[neighbor] = min(distances[neighbor], distance + 1)
                queue.append((neighbor, distances[neighbor]))
    return None