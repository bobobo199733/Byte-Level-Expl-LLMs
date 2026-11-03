def canFinish(num_courses, prerequisites):
    graph = {i: [] for i in range(num_courses)}
    for course, prereq in prerequisites:
        graph[course].append(prereq)

    def is_cyclic_util(course, visited, rec_stack):
        visited[course] = True
        rec_stack[course] = True
        for neighbor in graph[course]:
            if not visited[neighbor]:
                if is_cyclic_util(neighbor, visited, rec_stack):
                    return True
            elif rec_stack[neighbor]:
                return True
        rec_stack[course] = False
        return False
    visited = [False] * num_courses
    rec_stack = [False] * num_courses
    for i in range(num_courses):
        if not visited[i]:
            if is_cyclic_util(i, visited, rec_stack):
                return False
    return True