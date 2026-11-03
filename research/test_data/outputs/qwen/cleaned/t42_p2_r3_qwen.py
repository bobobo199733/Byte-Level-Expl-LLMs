def course_schedule(num_courses, prerequisites):
    if not isinstance(num_courses, int) or not all((isinstance(prereq, list) and len(prereq) == 2 for prereq in prerequisites)):
        raise ValueError('Invalid input')
    graph = {i: [] for i in range(num_courses)}
    indegree = [0] * num_courses
    for course, prereq in prerequisites:
        if not (0 <= course < num_courses and 0 <= prereq < num_courses):
            raise ValueError('Invalid input')
        graph[prereq].append(course)
        indegree[course] += 1
    queue = [i for i in range(num_courses) if indegree[i] == 0]
    visited = 0
    while queue:
        course = queue.pop(0)
        visited += 1
        for neighbor in graph[course]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    return visited == num_courses