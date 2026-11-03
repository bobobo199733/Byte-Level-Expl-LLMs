import collections

def course_schedule(num_courses, prerequisites):
    graph = collections.defaultdict(list)
    indegrees = [0] * num_courses
    for course, prerequisite in prerequisites:
        graph[prerequisite].append(course)
        indegrees[course] += 1
    queue = [i for i, degree in enumerate(indegrees) if degree == 0]
    while queue:
        current_course = queue.pop(0)
        num_courses -= 1
        if num_courses == 0:
            return True
        for prerequisite in graph[current_course]:
            indegrees[prerequisite] -= 1
            if indegrees[prerequisite] == 0:
                queue.append(prerequisite)
    return num_courses == 0