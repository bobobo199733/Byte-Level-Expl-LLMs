def topological_sort(graph):

    def dfs(node, visited, stack, adjacency_list):
        if node in visited:
            return False
        visited[node] = True
        for neighbor in adjacency_list[node]:
            if not dfs(neighbor, visited, stack, adjacency_list):
                return False
        stack.appendleft(node)
        return True
    visited = {}
    stack = []
    for node in graph:
        if node not in visited:
            if not dfs(node, visited, stack, graph):
                raise ValueError('Cycle detected in the graph.')
    if len(graph) != len(stack):
        raise ValueError('The given graph is not a DAG.')
    return list(stack)