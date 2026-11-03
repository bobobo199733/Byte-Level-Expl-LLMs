def dijkstra_shortest_path(graph, start):
    import heapq
    num_nodes = len(graph)
    distances = [float('inf')] * num_nodes
    distances[start] = 0
    priority_queue = [(0, start)]
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        if current_distance > distances[current_node]:
            continue
        for neighbor in range(num_nodes):
            weight = graph[current_node][neighbor]
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))
    return distances