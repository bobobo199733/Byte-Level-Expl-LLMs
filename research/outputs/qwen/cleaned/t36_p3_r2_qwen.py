def dijkstra_shortest_path(graph, start):
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    unvisited_nodes = set(graph.keys())
    while unvisited_nodes:
        current_min_node = None
        for node in unvisited_nodes:
            if current_min_node is None or distances[node] < distances[current_min_node]:
                current_min_node = node
        if distances[current_min_node] == float('infinity'):
            break
        unvisited_nodes.remove(current_min_node)
        for neighbor in graph[current_min_node]:
            distance = distances[current_min_node] + graph[current_min_node][neighbor]
            if distance < distances[neighbor]:
                distances[neighbor] = distance
    return distances