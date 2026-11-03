from collections import defaultdict, deque

def course_schedule(num_courses, prerequisites):
    """
    Validate if all courses can be completed based on prerequisites.

    Args:
        num_courses (int): Total number of courses.
        prerequisites (list[list[int]]): List of pairs (course, prerequisite).

    Returns:
        bool: True if all courses can be completed, False otherwise.
    """
    graph = defaultdict(list)
    visited = set()
    for course, prereq in prerequisites:
        graph[prereq].append(course)
    for i in range(1, num_courses + 1):
        if i not in visited and (not dfs(graph, i, visited, set())):
            return False
    return True

def dfs(graph, course, visited, current_path):
    """
    Perform Depth-First Search to detect cycles.

    Args:
        graph (dict): Adjacency list of the graph.
        course (int): Current course being visited.
        visited (set): Set of visited courses.
        current_path (set): Set of courses in the current path.

    Returns:
        bool: True if no cycle found, False otherwise.
    """
    if course in current_path:
        return False
    visited.add(course)
    current_path.add(course)
    for neighbor in graph[course]:
        if neighbor not in visited or not dfs(graph, neighbor, visited, current_path):
            return False
    current_path.remove(course)
    return True