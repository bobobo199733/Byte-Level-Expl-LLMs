from collections import defaultdict, deque

def topological_sort(graph):
    """
    Performs a topological sort on a directed acyclic graph.

    Args:
        graph (dict): A dictionary representing the adjacency list of the graph.

    Returns:
        list: The ordering as a list. If a cycle is detected, raises a ValueError.

    Raises:
        ValueError: If a cycle exists in the graph.
    """
    visited = set()
    stack = []
    incoming_edges = defaultdict(int)
    for node in graph:
        for neighbor in graph[node]:
            incoming_edges[neighbor] += 1

    def dfs(node):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                incoming_edges[neighbor] -= 1
                if incoming_edges[neighbor] == 0:
                    dfs(neighbor)
            elif neighbor in stack:
                raise ValueError('Cycle detected')
    for node in graph:
        if node not in visited and incoming_edges[node] == 0:
            dfs(node)
    while stack:
        node = stack.pop()
        if node not in visited:
            stack.appendleft(node)
            visited.add(node)
        else:
            stack.append(node)
    return list(stack)