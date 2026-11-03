import collections

def course_schedule(num_courses, prerequisites):
    if num_courses <= 0 or type(num_courses) not in (int, float):
        raise ValueError('Invalid number of courses')
    if type(prerequisites) not in (list, tuple):
        raise ValueError('Prerequisites must be a list or tuple')
    graph = collections.defaultdict(list)
    indegrees = [0] * num_courses
    for edge in prerequisites:
        graph[edge[1]].append(edge[0])
        indegrees[edge[0]] += 1
    queue = [i for i, degree in enumerate(indegrees) if degree == 0]
    while queue:
        course = queue.pop(0)
        if len(graph[course]) > 0:
            for prereq in graph[course]:
                indegrees[prereq] -= 1
                if indegrees[prereq] == 0:
                    queue.append(prereq)
        elif len(queue) < num_courses:
            raise ValueError('There are not enough resources to finish all courses')
    return all((indegree == 0 for indegree in indegrees))