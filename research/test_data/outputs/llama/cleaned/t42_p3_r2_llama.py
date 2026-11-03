from collections import defaultdict, deque

def course_schedule(num_courses, prerequisites):
    """
    Checks if all courses can be completed based on given prerequisites.

    Args:
        num_courses (int): Total number of courses.
        prerequisites (list): List of pairs where each pair represents a prerequisite for a course.

    Returns:
        bool: True if all courses can be completed; False otherwise.
    """
    graph = defaultdict(list)
    indegree = {i: 0 for i in range(num_courses)}
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        indegree[course] += 1
    queue = deque([course for course in indegree if indegree[course] == 0])
    while queue:
        course = queue.popleft()
        for neighbor in graph[course]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    return all((indegree[course] == 0 for course in range(num_courses)))