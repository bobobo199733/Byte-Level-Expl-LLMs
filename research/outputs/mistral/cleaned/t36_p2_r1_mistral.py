from heapq import heappush, heappop, heapify

def dijkstra_shortest_path(graph, start):
    INF = float('inf')
    n = len(graph)
    distances = [INF] * n
    visited = [False] * n
    distances[start] = 0
    priority_queue = [(0, start)]
    while priority_queue:
        current_distance, current_node = heappop(priority_queue)
        if visited[current_node]:
            continue
        visited[current_node] = True
        for neighbor, weight in graph[current_node]:
            if not visited[neighbor]:
                new_distance = current_distance + weight
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    heappush(priority_queue, (new_distance, neighbor))
    return {node: distance for node, distance in enumerate(distances) if 0 <= distance < INF}