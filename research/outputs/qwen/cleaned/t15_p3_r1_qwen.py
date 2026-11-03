def dfs(graph, node, visited, stack):
    if not visited[node]:
        visited[node] = True
        for neighbor in graph[node]:
            dfs(graph, neighbor, visited, stack)
        stack.append(node)

def topological_sort(graph):
    from collections import defaultdict
    visited = defaultdict(bool)
    stack = []
    for node in graph:
        if not visited[node]:
            dfs(graph, node, visited, stack)
    return stack[::-1]