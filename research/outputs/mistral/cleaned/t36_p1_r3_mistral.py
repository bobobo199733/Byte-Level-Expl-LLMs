def dijkstra_shortest_path(graph, start):
    import heapq
    INF = float('inf')
    n = len(graph)
    distances = [INF] * n
    distances[start] = 0
    shortest_path = {}
    unvisited = set(range(n))
    smallheap = []
    heapq.heappush(smallheap, (0, start))
    while unvisited:
        current_distance, current_node = heapq.heappop(smallheap)
        for neighbor, weight in enumerate(graph[current_node]):
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(smallheap, (distance, neighbor))
                shortest_path[neighbor] = current_node
        unvisited.remove(current_node)
    return (distances, shortest_path)