from collections import defaultdict, deque

def topological_sort(graph):
    """
    Performs a topological sort on a directed acyclic graph (DAG).

    Args:
        graph: A dictionary representing the adjacency list of the graph.
            Each key is a node in the graph, and its corresponding value is a list
            of neighboring nodes.

    Returns:
        A valid topological ordering of the DAG as a list of nodes.
    """
    in_degree = defaultdict(int)
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            in_degree[neighbor] += 1
    queue = deque([node for node in graph if in_degree[node] == 0])
    result = []
    while queue:
        node = queue.popleft()
        result.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    if len(result) != len(graph):
        raise ValueError('Graph contains cycles; cannot perform topological sort')
    return result