from collections import defaultdict, deque

def course_schedule(num_courses, prerequisites):
    """
    Checks if all courses can be completed given the number of courses and their prerequisites.

    Args:
        num_courses (int): Total number of courses.
        prerequisites (list[list[int]]): A list of pairs where each pair contains a prerequisite course and its corresponding course.

    Returns:
        bool: True if all courses can be completed, False otherwise.
    """
    graph = defaultdict(list)
    in_degree = {i: 0 for i in range(num_courses)}
    for u, v in prerequisites:
        graph[u].append(v)
        in_degree[v] += 1
    queue = deque([course for course in in_degree if in_degree[course] == 0])
    while queue:
        course = queue.popleft()
        for neighbor in graph[course]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    return all((in_degree[course] == 0 for course in range(num_courses)))