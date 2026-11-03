def bfs_shortest_path(graph, start, target):
    visited = set()
    queue = [(start, 0)]
    while queue:
        node, distance = queue.pop(0)
        if node in visited:
            continue
        visited.add(node)
        if node == target:
            return distance
        for neighbor in graph[node]:
            queue.append((neighbor, distance + 1))
    return -1