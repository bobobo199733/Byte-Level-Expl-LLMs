from typing import Dict, List, Tuple

def bfs_shortest_path(graph: Dict[int, List[int]], start: int, target: int) -> int:
    """
    This function performs a breadth-first search (BFS) on an unweighted graph and returns the shortest distance between two nodes.

    Args:
        graph: A dictionary representing the adjacency list of the graph.
        start: The node where the BFS traversal begins.
        target: The target node for which we want to find the shortest distance from the start node.

    Returns:
        An integer representing the shortest distance between the start and target nodes. If no path exists, returns -1.
    """
    queue = [start]
    visited = {start}
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    while queue:
        current_node = queue.pop(0)
        if current_node == target:
            return distances[current_node]
        for neighbor in graph.get(current_node, []):
            if neighbor not in visited:
                distances[neighbor] = min(distances[neighbor], 1 + distances[current_node])
                queue.append(neighbor)
                visited.add(neighbor)
    return -1