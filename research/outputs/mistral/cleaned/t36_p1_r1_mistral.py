def dijkstra_shortest_path(graph, start):
    n = len(graph)
    dist = [float('inf')] * n
    visited = [False] * n
    dist[start] = 0
    for _ in range(n - 1):
        min_distance = float('inf')
        u = -1
        for node in range(n):
            if not visited[node] and dist[node] < min_distance:
                min_distance = dist[node]
                u = node
        visited[u] = True
        for neighbor in graph[u]:
            if not visited[neighbor]:
                new_dist = dist[u] + 1
                if new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist
    return dist