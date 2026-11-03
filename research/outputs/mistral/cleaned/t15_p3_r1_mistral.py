from collections import defaultdict, deque

def topological_sort(graph):
    indegree = defaultdict(int)
    successors = defaultdict(list)
    for node in graph:
        for neighbor in graph[node]:
            successors[neighbor].append(node)
            indegree[node] += 1
    queue = deque([node for node in graph if indegree[node] == 0])
    result = []
    while queue:
        current_node = queue.popleft()
        result.append(current_node)
        for neighbor in successors[current_node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    return result if not result else None