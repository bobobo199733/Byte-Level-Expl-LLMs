def topological_sort(graph):
    indegrees = {node: 0 for node in graph}
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            indegrees[neighbor] += 1
    from collections import deque
    queue = deque([node for node in graph if indegrees[node] == 0])
    result = []
    while queue:
        current_node = queue.popleft()
        result.append(current_node)
        for neighbor in graph[current_node]:
            indegrees[neighbor] -= 1
            if indegrees[neighbor] == 0:
                queue.append(neighbor)
    if len(result) != len(graph):
        raise ValueError('Cycle detected or graph is not a DAG')
    return result