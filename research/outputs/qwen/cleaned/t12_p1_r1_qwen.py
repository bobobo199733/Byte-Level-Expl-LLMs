from collections import deque

def bfs_shortest_path(graph, start, target):
    """
    Perform a Breadth-First Search (BFS) in an unweighted graph and return the length of the shortest path between 
    the start node and the target node.

    :param graph: A dictionary representing the adjacency list of the graph.
    :param start: The starting node.
    :param target: The target node.
    :return: The length of the shortest path from start to target, or -1 if no path exists.
    """
    queue = deque([(start, 0)])
    visited = {start}
    while queue:
        current_node, distance = queue.popleft()
        if current_node == target:
            return distance
        for neighbor in graph.get(current_node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, distance + 1))
    return -1