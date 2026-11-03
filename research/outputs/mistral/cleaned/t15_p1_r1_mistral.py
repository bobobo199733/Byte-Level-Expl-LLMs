from collections import defaultdict

def topological_sort(graph):
    indegrees = defaultdict(int)
    successors = defaultdict(set)
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            successors[neighbor].add(node)
            indegrees[node] += 1
    zero_indegree_nodes = set((n for n in graph if indegrees[n] == 0))
    sorted_nodes = []
    while zero_indegree_nodes:
        current_node = zero_indegree_nodes.pop()
        sorted_nodes.append(current_node)
        for neighbor in successors[current_node]:
            indegrees[neighbor] -= 1
            if indegrees[neighbor] == 0:
                zero_indegree_nodes.add(neighbor)
    if len(sorted_nodes) != len(graph):
        raise ValueError('Graph has a cycle')
    return sorted_nodes