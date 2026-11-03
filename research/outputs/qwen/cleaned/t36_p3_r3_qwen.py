def dijkstra_shortest_path(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]
    while priority_queue:
        current_distance, current_node = min(priority_queue, key=lambda x: x[0])
        priority_queue.remove((current_distance, current_node))
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                priority_queue.remove((distances[neighbor], neighbor))
                distances[neighbor] = distance
                priority_queue.append((distance, neighbor))
    return distances