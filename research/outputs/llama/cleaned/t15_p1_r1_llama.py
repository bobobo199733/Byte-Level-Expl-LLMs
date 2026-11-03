def topological_sort(graph):
    """
    Returns a valid topological ordering of a directed acyclic graph.
    
    Args:
        graph: A dictionary representing the graph, where each key is a node
            and its corresponding value is a list of neighboring nodes.
    
    Returns:
        A list representing a valid topological ordering of the graph. If the
        input graph contains cycles, an empty list is returned.
    """
    order = []
    visited = set()
    in_degree = {node: 0 for node in graph}
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1

    def dfs(node):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)
        order.append(node)
    for node in in_degree:
        if in_degree[node] == 0:
            dfs(node)
    if len(order) != len(graph):
        return []
    return order[::-1]