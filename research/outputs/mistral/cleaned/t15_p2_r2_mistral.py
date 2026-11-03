def topological_sort(graph):

    def dfs(node, visited, stack, rec_stack=None):
        if rec_stack is None:
            rec_stack = []
        visited[node] = True
        for neighbour in graph[node]:
            if not visited[neighbour]:
                dfs(neighbour, visited, stack, rec_stack)
            elif neighbour in rec_stack:
                raise ValueError('Cycle detected.')
        stack.append(node)
        rec_stack.remove(node) if node in rec_stack else None
    visited = {node: False for node in graph}
    stack = []
    for node in graph:
        if not visited[node]:
            dfs(node, visited, stack)
    return list(reversed(stack)) if stack else None