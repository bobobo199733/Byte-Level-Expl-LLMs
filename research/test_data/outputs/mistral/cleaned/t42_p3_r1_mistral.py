from collections import defaultdict
import copy

def course_schedule(num_courses, prerequisites):
    graph = build_graph(num_courses, prerequisites)
    ordered_courses = topological_sort(graph)
    if not ordered_courses or len(ordered_courses) < num_courses:
        return False
    return True

def build_graph(num_courses, prerequisites):
    graph = defaultdict(list)
    for edge in prerequisites:
        course_1, course_2 = edge
        graph[course_2].append(course_1)
    return graph

def topological_sort(graph):
    indegree = dict(((node, 0) for node in graph))
    for node in graph:
        for neighbor in graph[node]:
            indegree[neighbor] += 1
    queue = [node for node in graph if indegree[node] == 0]
    ordered_courses = []
    while queue:
        current_course = queue.pop(0)
        ordered_courses.append(current_course)
        for neighbor in graph[current_course]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    return ordered_courses