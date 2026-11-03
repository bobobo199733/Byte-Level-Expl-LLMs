def topological_sort(graph):
    in_degrees = {node: 0 for node in graph}
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            in_degrees[neighbor] += 1
    from collections import deque
    queue = deque([node for node, degree in in_degrees.items() if degree == 0])
    topological_order = []
    while queue:
        node = queue.popleft()
        topological_order.append(node)
        for neighbor in graph[node]:
            in_degrees[neighbor] -= 1
            if in_degrees[neighbor] == 0:
                queue.append(neighbor)
        if len(topological_order) < len(in_degrees):
            raise ValueError('Graph contains a cycle')
    return topological_order