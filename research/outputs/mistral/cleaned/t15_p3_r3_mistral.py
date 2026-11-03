from collections import defaultdict

def topological_sort(graph):
    indegree = defaultdict(int)
    for node in graph:
        for neighbor in graph[node]:
            indegree[neighbor] += 1
    queue = [node for node in graph if indegree[node] == 0]
    sorted_nodes = []
    while queue:
        current_node = queue.pop()
        sorted_nodes.append(current_node)
        for neighbor in graph[current_node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    if len(sorted_nodes) != len(graph):
        print('The given graph is not a Directed Acyclic Graph (DAG).')
        return None
    return sorted_nodes