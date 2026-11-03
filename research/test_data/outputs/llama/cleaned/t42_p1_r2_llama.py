from collections import defaultdict

def course_schedule(num_courses, prerequisites):
    """
    Determines whether all courses can be completed.

    Args:
        num_courses (int): The total number of courses.
        prerequisites (list): A list of prerequisite pairs [a, b] where a depends on b.

    Returns:
        bool: True if all courses can be completed, otherwise False.
    """
    graph = defaultdict(list)
    in_degree = {i: 0 for i in range(num_courses)}
    for prerequisite in prerequisites:
        a, b = prerequisite
        graph[b].append(a)
        in_degree[a] += 1
    queue = [i for i in range(num_courses) if in_degree[i] == 0]
    while queue:
        course = queue.pop(0)
        for neighbor in graph[course]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    for degree in in_degree.values():
        if degree != 0:
            return False
    return True