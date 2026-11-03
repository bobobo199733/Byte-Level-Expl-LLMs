from collections import defaultdict, deque

def course_schedule(num_courses, prerequisites):
    """
    Determine whether all courses can be completed based on given prerequisites.

    Args:
        num_courses (int): The total number of courses.
        prerequisites (list[list[int]]): Each inner list contains a prerequisite pair [a, b] meaning course a depends on course b.

    Returns:
        bool: True if all courses can be completed, otherwise False.
    """
    graph = defaultdict(list)
    in_degree = {i: 0 for i in range(num_courses)}
    for a, b in prerequisites:
        graph[b].append(a)
        in_degree[a] += 1
    queue = deque([i for i in in_degree if in_degree[i] == 0])
    while queue:
        course = queue.popleft()
        for neighbor in graph[course]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    return all((in_degree[i] == 0 for i in in_degree))