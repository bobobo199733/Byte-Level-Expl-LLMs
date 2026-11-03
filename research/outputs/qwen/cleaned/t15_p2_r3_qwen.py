def topological_sort(graph):

    def dfs(node, graph, path, visited, order):
        visited[node] = True
        for neighbor in graph.get(node, []):
            if not visited[neighbor]:
                dfs(neighbor, graph, path, visited, order)
        order.appendleft(node)
    visited = {node: False for node in graph}
    order = []
    for node in graph:
        if not visited[node]:
            dfs(node, graph, path=order, visited=visited, order=order)
    return list(order)