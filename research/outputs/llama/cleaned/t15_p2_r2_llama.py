def topological_sort(graph):
    """
    Performs a topological sort on a directed acyclic graph.

    Args:
        graph (dict): A dictionary representing the adjacency list of the graph.

    Returns:
        list: A list containing the nodes in a valid topological order.

    Raises:
        ValueError: If the graph contains cycles.
    """
    visited = set()
    current_path = set()
    result = []

    def dfs(node):
        """
        Performs depth-first search on a node.

        Args:
            node: The node to start the DFS from.
        """
        visited.add(node)
        current_path.add(node)
        for neighbor in graph.get(node, []):
            if neighbor in current_path:
                raise ValueError('Cycle detected')
            if neighbor not in visited:
                dfs(neighbor)
        current_path.remove(node)
        result.append(node)
    for node in graph:
        if node not in visited:
            dfs(node)
    return result