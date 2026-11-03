def bfs_shortest_path(graph, start, target):
    if not graph or not isinstance(graph, dict) or (not start) or (not target):
        return -1
    visited = set()
    queue = [(start, [], 0)]
    while queue:
        node, path, distance = queue.pop(0)
        if node == target:
            return distance
        if node in visited:
            continue
        visited.add(node)
        for neighbor in graph[node]:
            new_path = path + [node]
            queue.append((neighbor, new_path, distance + 1))
    return -1