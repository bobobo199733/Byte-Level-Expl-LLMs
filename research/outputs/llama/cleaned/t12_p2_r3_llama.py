from collections import deque

def bfs_shortest_path(graph, start, target):
    """
    Compute the shortest distance between two nodes in an unweighted graph using breadth-first search.

    Args:
    - graph: An adjacency list representation of the graph.
    - start: The node to start from.
    - target: The target node.

    Returns:
    - The shortest distance between the start and target nodes, or -1 if no path exists.

    Raises:
    - ValueError: If the graph is empty or if the start or target nodes are not in the graph.
    """
    if not graph or start not in graph or target not in graph:
        raise ValueError('Invalid graph or node')
    queue = deque([(start, 0)])
    visited = set()
    current_level = set([start])
    while queue:
        for _ in range(len(current_level)):
            node, distance = current_level.pop()
            if node == target:
                return distance
            visited.add(node)
            for neighbor in graph[node]:
                if neighbor not in visited and neighbor not in current_level:
                    queue.append((neighbor, distance + 1))
                    current_level.add(neighbor)
        current_level = set(queue)[0][::2]
    return -1