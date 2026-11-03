from collections import defaultdict

def topological_sort(graph):
    in_degrees = defaultdict(int)
    for neighbors in graph.values():
        for neighbor in neighbors:
            in_degrees[neighbor] += 1
    queue = [node for node in graph if in_degrees[node] == 0]
    top_order = []
    while queue:
        node = queue.pop(0)
        top_order.append(node)
        for neighbor in graph[node]:
            in_degrees[neighbor] -= 1
            if in_degrees[neighbor] == 0:
                queue.append(neighbor)
    return top_order