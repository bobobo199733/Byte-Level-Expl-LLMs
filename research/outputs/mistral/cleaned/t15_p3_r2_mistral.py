def topological_sort(graph):
    visited, indegree, order = (set(), {node: 0 for node in graph}, [])

    def dfs(node):
        if node not in visited:
            visited.add(node)
            for neighbor in graph[node]:
                indegree[neighbor] -= 1
                if indegree[neighbor] == 0:
                    dfs(neighbor)
                    order.append(neighbor)
    for node in graph:
        if indegree[node] == 0:
            dfs(node)
    return list(reversed(order))