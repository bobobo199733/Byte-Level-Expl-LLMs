from collections import deque

def bfs_shortest_path(graph, start, target):
    if start not in graph or target not in graph:
        return -1
    visited = set()
    queue = deque([(start, 0)])
    visited.add(start)
    while queue:
        current_node, distance = queue.popleft()
        if current_node == target:
            return distance
        for neighbor in graph[current_node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, distance + 1))
    return -1