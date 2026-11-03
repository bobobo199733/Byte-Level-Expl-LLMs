def dijkstra_shortest_path(graph, start):
    import heapq
    inf = float('inf')
    distances = {node: inf for node in graph}
    distances[start] = 0
    shortest_path = {}
    unvisited = set(graph)
    priority_queue = list(map(lambda node: (distances[node], node), unvisited))
    heapq.heapify(priority_queue)
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        if current_distance > distances[current_node]:
            continue
        unvisited.remove(current_node)
        for neighbor, weight in graph[current_node]:
            distance = distances[current_node] + weight
            if distance < distances.get(neighbor, inf):
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))
                shortest_path[neighbor] = current_node
    return (distances, shortest_path)