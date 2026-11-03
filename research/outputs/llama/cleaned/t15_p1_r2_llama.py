from collections import defaultdict, deque

def topological_sort(graph):
    """
    Returns a valid topological ordering of a directed acyclic graph.

    Args:
        graph: A dictionary representing the adjacency list of the graph.
            Each key is a node in the graph, and its corresponding value is a list
            of its neighbors.

    Returns:
        A list of nodes representing a valid topological ordering of the graph.
    """
    visited = set()
    in_degree = defaultdict(int)
    queue = deque()
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1
    for node in graph:
        if in_degree[node] == 0:
            queue.append(node)
            visited.add(node)
    result = []
    while queue:
        node = queue.popleft()
        result.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
                visited.add(neighbor)
    if len(result) != len(graph):
        raise ValueError('The input graph is not a directed acyclic graph')
    return result