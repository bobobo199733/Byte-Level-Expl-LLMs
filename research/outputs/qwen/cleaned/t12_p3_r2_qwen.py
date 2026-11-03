from collections import deque

def bfs_shortest_path(graph, start, target):
    """
    Perform BFS to find the shortest path from 'start' to 'target' node in a graph.
    
    :param graph: A dictionary representing the graph where keys are nodes and values are lists of adjacent nodes.
    :param start: The starting node for the search.
    :param target: The target node to reach.
    :return: The shortest distance (number of edges) from 'start' to 'target'. Returns -1 if there is no path.
    """
    if not isinstance(graph, dict) or start not in graph or target not in graph:
        return 'Invalid input'
    queue = deque([(start, 0)])
    visited = set()
    while queue:
        current_node, distance = queue.popleft()
        if current_node == target:
            return distance
        if current_node in visited:
            continue
        visited.add(current_node)
        for neighbor in graph[current_node]:
            if neighbor not in visited:
                queue.append((neighbor, distance + 1))
    return -1