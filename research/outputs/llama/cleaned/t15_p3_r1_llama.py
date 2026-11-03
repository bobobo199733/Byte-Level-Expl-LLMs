from collections import defaultdict, deque

def topological_sort(graph):
    """
    Performs a topological sorting on a directed acyclic graph (DAG).

    Args:
        graph: A dictionary representing the adjacency list of the DAG.
            Each key is a node and its value is a set or list of adjacent nodes.

    Returns:
        A list of nodes in topologically sorted order. If a cycle exists,
        an empty list is returned.

    Example:
        >>> graph = {'A': ['B', 'C'], 'B': ['D'], 'C': ['D'], 'D': []}
        >>> print(topological_sort(graph))
        ['D', 'B', 'C', 'A']
    """
    in_degree = {node: 0 for node in graph}
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1
    queue = deque([node for node, degree in in_degree.items() if degree == 0])
    sorted_nodes = []
    while queue:
        node = queue.popleft()
        sorted_nodes.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    if len(sorted_nodes) != len(graph):
        return []
    return sorted_nodes