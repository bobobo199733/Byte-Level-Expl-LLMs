from collections import defaultdict, deque

def canFinish(numCourses, prerequisites):
    graph = defaultdict(list)
    visited = [False] * numCourses
    degree = [0] * numCourses
    for edge in prerequisites:
        graph[edge[1]].append(edge[0])
        degree[edge[0]] += 1
    queue = deque()
    for course in range(numCourses):
        if degree[course] == 0:
            queue.append(course)
    finished_courses = 0
    while queue:
        current_course = queue.popleft()
        visited[current_course] = True
        finished_courses += 1
        for neighbor in graph[current_course]:
            degree[neighbor] -= 1
            if degree[neighbor] == 0:
                queue.append(neighbor)
    return finished_courses == numCourses