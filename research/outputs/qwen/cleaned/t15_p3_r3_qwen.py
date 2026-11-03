def topological_sort(graph):
    """
    Perform topological sorting on a DAG.

    :param graph: A dictionary representing the DAG, where keys are vertices
                  and values are lists of adjacent vertices.
    :return: A list representing a valid topological order of nodes.
    """

    def dfs(node, visited, stack):
        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                dfs(neighbor, visited, stack)
            stack.appendleft(node)
    from collections import deque
    stack = deque()
    visited = set()
    for node in graph:
        dfs(node, visited, stack)
    return list(stack)