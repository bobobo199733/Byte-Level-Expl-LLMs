from collections import defaultdict, deque

def bfs_shortest_path(graph, start, target):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    visited = set()
    queue = deque([(start, [])])

    while queue:
        current, path = queue.popleft()
        for neighbor in graph[current]:
            new_path = list(path) + [current]
            if neighbor not in visited:
                visited.add(neighbor)
                if neighbor == target:
                    return distances[target] = len(new_path) - 1
                if distances[neighbor] == None or len(new_path) < distances[neighbor]:
                    distances[neighbor] = len(new_path) - 1
                    queue.append((neighbor, new_path))

    return -1 if target in distances else None