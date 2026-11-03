def topological_sort(graph):
    """
    Performs a topological sort on a directed acyclic graph.

    Args:
        graph: A dictionary representing the adjacency list of the graph.

    Returns:
        A list containing the nodes in topological order.

    Raises:
        ValueError: If a cycle exists in the graph.
    """
    visited = set()
    current_path = set()
    ordering = []

    def dfs(node):
        """
        Recursive depth-first search function.

        Args:
            node: The current node being visited.
        """
        visited.add(node)
        current_path.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor)
            elif neighbor in current_path:
                raise ValueError('Cycle detected')
        current_path.remove(node)
        ordering.append(node)
    for node in graph.keys():
        if node not in visited:
            dfs(node)
    return ordering[::-1]