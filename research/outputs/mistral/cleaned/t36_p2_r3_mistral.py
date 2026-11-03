from heapq import heappush, heappop, heapify

def dijkstra_shortest_path(graph, start):
    inf = float('inf')
    n = len(graph)
    dist = [inf] * n
    dist[start] = 0
    visited = set()
    queue = [(0, start)]
    while queue:
        d, current = heappop(queue)
        if current in visited:
            continue
        visited.add(current)
        for neighbor, weight in graph[current].items():
            if neighbor not in visited and dist[neighbor] > dist[current] + weight:
                dist[neighbor] = dist[current] + weight
                heappush(queue, (dist[neighbor], neighbor))
    return dist