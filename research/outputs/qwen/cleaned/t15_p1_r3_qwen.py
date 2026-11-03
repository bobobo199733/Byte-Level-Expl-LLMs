from collections import defaultdict, deque

def topological_sort(graph):
    in_degrees = {node: 0 for node in graph}
    sorted_order = []
    for node in graph:
        for neighbor in graph[node]:
            in_degrees[neighbor] += 1
    sources = deque([node for node, degree in in_degrees.items() if degree == 0])
    while sources:
        current_node = sources.popleft()
        sorted_order.append(current_node)
        for neighbor in graph[current_node]:
            in_degrees[neighbor] -= 1
            if in_degrees[neighbor] == 0:
                sources.append(neighbor)
    if len(sorted_order) != len(graph):
        raise ValueError('There is a cycle in the graph')
    return sorted_order