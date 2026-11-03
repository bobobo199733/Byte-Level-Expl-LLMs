from collections import defaultdict

def course_schedule(num_courses, prerequisites):
    graph = defaultdict(list)
    indegrees = [0] * num_courses
    for prerequisite in prerequisites:
        graph[prerequisite[1]].append(prerequisite[0])
        indegrees[prerequisite[0]] += 1
    queue = [i for i, degree in enumerate(indegrees) if degree == 0]
    schedule = []
    while queue:
        course = queue.pop(0)
        schedule.append(course)
        for prerequisite in graph[course]:
            indegrees[prerequisite] -= 1
            if indegrees[prerequisite] == 0:
                queue.append(prerequisite)
    return len(schedule) == num_courses