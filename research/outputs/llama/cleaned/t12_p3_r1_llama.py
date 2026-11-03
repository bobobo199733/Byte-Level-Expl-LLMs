from collections import deque

def bfs_shortest_path(graph, start, target):
    """
    This function uses Breadth-First Search (BFS) to find the shortest path between 
    two nodes in an undirected graph.

    Args:
        graph: A dictionary representing the adjacency list of the graph.
        start: The node from which to start the search.
        target: The node we are trying to reach.

    Returns:
        int: The length of the shortest path between start and target, or -1 if there is no such path.
    """
    queue = deque([(start, 0)])
    visited = set()
    while queue:
        current_node, distance = queue.popleft()
        if current_node == target:
            return distance
        visited.add(current_node)
        for neighbor in graph.get(current_node, []):
            if neighbor not in visited:
                queue.append((neighbor, distance + 1))
    return -1