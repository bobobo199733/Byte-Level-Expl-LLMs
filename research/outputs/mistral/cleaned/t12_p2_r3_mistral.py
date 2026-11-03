def bfs_shortest_path(graph, start, target):
    visited = set()
    queue = [(start, 0)]
    shortest_distances = {node: float('inf') for node in graph}
    shortest_distances[start] = 0
    while queue:
        current_node, current_distance = queue.pop(0)
        visited.add(current_node)
        if current_node == target:
            return current_distance
        for neighbor in graph[current_node]:
            if neighbor not in visited:
                shortest_distances[neighbor] = min(shortest_distances[neighbor], current_distance + 1)
                queue.append((neighbor, shortest_distances[neighbor]))
    return -1