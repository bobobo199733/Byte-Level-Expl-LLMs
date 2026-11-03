def dijkstra_shortest_path(graph, start):
    import heapq
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    shortest_queue = [(0, start)]
    while shortest_queue:
        current_distance, current_node = heapq.heappop(shortest_queue)
        if current_distance > distances[current_node]:
            continue
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(shortest_queue, (distance, neighbor))
    return distances