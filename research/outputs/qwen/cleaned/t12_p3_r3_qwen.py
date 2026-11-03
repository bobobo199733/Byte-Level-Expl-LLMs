from collections import deque

def bfs_shortest_path(graph, start, target):
    """
    Perform BFS to find the shortest path from 'start' to 'target' in the graph.
    
    :param graph: A dictionary representing the adjacency list of the graph
    :param start: The starting node
    :param target: The target node
    :return: The shortest distance (number of edges) or None if no path exists
    """
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    queue = deque([start])
    while queue:
        current_node = queue.popleft()
        for neighbor in graph[current_node]:
            if distances[neighbor] == float('inf'):
                distances[neighbor] = distances[current_node] + 1
                queue.append(neighbor)
                if neighbor == target:
                    return distances[target]
    return None