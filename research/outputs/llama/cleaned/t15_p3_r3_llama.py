from collections import defaultdict, deque

def topological_sort(graph):
    """
    Performs a topological sort on a directed acyclic graph.

    Args:
        graph: A dictionary representing the adjacency list of the graph.
               Each key is a node and its corresponding value is a list of its neighbors.

    Returns:
        A list of nodes in a topologically sorted order.
    """
    in_degree = defaultdict(int)
    for node in graph:
        in_degree[node] = 0
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] += 1
    queue = deque([node for node in graph if in_degree[node] == 0])
    sorted_nodes = []
    while queue:
        node = queue.popleft()
        sorted_nodes.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    if len(sorted_nodes) != len(graph):
        raise ValueError('The graph contains a cycle and cannot be topologically sorted.')
    return sorted_nodes