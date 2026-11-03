from collections import defaultdict, deque

def topological_sort(graph):
    in_degree = defaultdict(int)
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            in_degree[neighbor] += 1

    zero_in_degree_queue = deque([node for node in graph if in_degree[node] == 0])

    result = []

    while zero_in_degree_queue:
        current_node = zero_in_degree_queue.popleft()
        result.append(current_node)

        for neighbor in graph[current_node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                zero_in_degree_queue.append(neighbor)

    return result if not result else None

# Example usage:
graph = {
    'A': ['B', 'D'],
    'B': ['C'],
    'C': [],
    'D': ['E']
    'E': []
}
print(topological_sort(graph))  # Output: ['C', 'B', 'A', 'D', 'E']