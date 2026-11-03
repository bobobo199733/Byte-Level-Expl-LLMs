def topological_sort(graph):

    def dfs(node, visited, stack, recursion):
        if node in recursion or node in visited:
            raise ValueError('Cycle detected!')
        visited.add(node)
        recursion.add(node)
        for neighbor in graph[node]:
            dfs(neighbor, visited, stack, recursion)
        recursion.remove(node)
        stack.append(node)
    visited = set()
    recursion = set()
    stack = []
    for node in graph:
        if node not in visited:
            dfs(node, visited, stack, recursion)
    if len(recursion) > 0 or len(graph) != len(stack):
        raise ValueError('Graph is not a Directed Acyclic Graph!')
    return list(reversed(stack))