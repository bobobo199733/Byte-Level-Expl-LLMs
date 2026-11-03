from collections import defaultdict

def course_schedule(num_courses, prerequisites):
    graph = defaultdict(list)
    for course, prereq in prerequisites:
        graph[prereq].append(course)
    visiting_status = [0] * num_courses

    def is_cyclic(node):
        if visiting_status[node] == 1:
            return True
        if visiting_status[node] == 2:
            return False
        visiting_status[node] = 1
        for neighbor in graph[node]:
            if is_cyclic(neighbor):
                return True
        visiting_status[node] = 2
        return False
    for course in range(num_courses):
        if is_cyclic(course):
            return False
    return True