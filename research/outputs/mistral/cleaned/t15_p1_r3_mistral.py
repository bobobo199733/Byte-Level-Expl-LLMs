def topological_sort(graph):
    visited = set()
    stack = []
    for node in graph:
        if node not in visited:
            dfs(node, graph, visited, stack)
    return list(reversed(stack))

def dfs(node, graph, visited, stack):
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(neighbor, graph, visited, stack)
    stack.append(node)