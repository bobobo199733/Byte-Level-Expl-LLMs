from collections import deque

def bfs_shortest_path(graph, start, target):
    """
    Perform BFS to find the shortest path from 'start' to 'target' node.
    
    :param graph: An adjacency list representing the graph.
    :param start: The starting node for the search.
    :param target: The target node to find the path to.
    :return: A tuple containing the distance and the list of nodes in the shortest path.
             If there is no path, returns (None, None).
    """
    queue = deque()
    visited = {start: None}
    queue.append((start, 0))
    while queue:
        current_node, distance = queue.popleft()
        if current_node == target:
            path = []
            temp = current_node
            while temp is not None:
                path.append(temp)
                temp = visited[temp]
            return (distance, list(reversed(path)))
        for neighbor in graph[current_node]:
            if neighbor not in visited:
                visited[neighbor] = current_node
                queue.append((neighbor, distance + 1))
    return (None, None)