def dijkstra_shortest_path(graph, start):
    n = len(graph)
    shortest_paths = [float('inf')] * n
    visited = [False] * n
    shortest_paths[start] = 0
    for _ in range(n - 1):
        min_distance = float('inf')
        current_node = None
        for node in range(n):
            if not visited[node] and shortest_paths[node] < min_distance:
                min_distance = shortest_paths[node]
                current_node = node
        visited[current_node] = True
        for neighbor in range(n):
            if graph[current_node][neighbor] != float('inf') and (not visited[neighbor]):
                new_distance = shortest_paths[current_node] + graph[current_node][neighbor]
                if new_distance < shortest_paths[neighbor]:
                    shortest_paths[neighbor] = new_distance
    return shortest_paths