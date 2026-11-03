def course_schedule(num_courses, prerequisites):
    """
    Determines whether it is possible to finish all courses given prerequisite dependencies.

    Args:
        num_courses (int): The number of courses.
        prerequisites (list[list[int]]): A list of pairs (course, prerequisite) where course takes the course and can take the prerequisite.

    Returns:
        bool: True if all courses can be completed, False otherwise.
    """
    if num_courses < 0 or len(prerequisites) < 0:
        raise ValueError('Invalid input')
    graph = [[] for _ in range(num_courses)]
    in_degree = [0] * num_courses
    for u, v in prerequisites:
        graph[v].append(u)
        in_degree[u] += 1
    queue = [i for i in range(num_courses) if in_degree[i] == 0]
    while queue:
        u = queue.pop(0)
        for v in graph[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)
    return all((degree == 0 for degree in in_degree))