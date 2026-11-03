def bfs_shortest_path(graph, start, target):
    visited = set()
    queue = [(start, [], 0)]
    while queue:
        node, path, distance = queue.pop(0)
        if node == target:
            return distance
        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                new_path = list(path) + [neighbor]
                new_distance = distance + 1
                queue.append((neighbor, new_path, new_distance))
    return None