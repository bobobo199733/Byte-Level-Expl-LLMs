def topological_sort(graph):
    if not graph:
        return []
    in_degrees = {node: 0 for node in graph}
    zero_in_degree_queue = []
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            in_degrees[neighbor] += 1
    for node in graph:
        if in_degrees[node] == 0:
            zero_in_degree_queue.append(node)
    top_order = []
    while zero_in_degree_queue:
        current_node = zero_in_degree_queue.pop(0)
        top_order.append(current_node)
        for neighbor in graph.get(current_node, []):
            in_degrees[neighbor] -= 1
            if in_degrees[neighbor] == 0:
                zero_in_degree_queue.append(neighbor)
    if len(top_order) != len(graph):
        raise ValueError('The graph contains a cycle and cannot be topologically sorted.')
    return top_order