from collections import defaultdict

def topological_sort(graph):
    in_degree = {node: 0 for node in graph}
    for u in graph:
        for v in graph[u]:
            in_degree[v] += 1
    queue = [node for node, degree in in_degree.items() if degree == 0]
    result = []
    while queue:
        current_node = queue.pop(0)
        result.append(current_node)
        for neighbor in graph[current_node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    if len(result) == len(graph):
        return result
    else:
        raise ValueError('Graph is not a Directed Acyclic Graph (DAG)')