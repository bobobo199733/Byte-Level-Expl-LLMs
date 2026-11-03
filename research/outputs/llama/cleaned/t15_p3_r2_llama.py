from collections import defaultdict, deque

def topological_sort(graph):
    """
    Returns a topological ordering of a Directed Acyclic Graph (DAG).

    Args:
        graph: A dictionary representing the adjacency list of the DAG.
            Each key is a node and its corresponding value is a list of its neighbors.

    Returns:
        A list representing the nodes in topological order.
    """
    visited = set()
    sources = deque()
    in_degree = defaultdict(int)
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            in_degree[neighbor] += 1
        if in_degree[node] == 0:
            sources.append(node)
            visited.add(node)
    ordering = []
    while sources:
        node = sources.popleft()
        ordering.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                sources.append(neighbor)
                visited.add(neighbor)
    if len(ordering) != len(graph):
        raise ValueError('The graph contains a cycle')
    return ordering