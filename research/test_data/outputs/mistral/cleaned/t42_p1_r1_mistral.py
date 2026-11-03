from collections import defaultdict

def course_schedule(num_courses, prerequisites):
    graph = defaultdict(list)
    indegree = [0] * num_courses
    for a, b in prerequisites:
        graph[b].append(a)
        indegree[a] += 1
    stack = []
    visited = set()
    for course in range(num_courses):
        if indegree[course] == 0 and course not in visited:
            dfs(course, graph, visited, stack)
    return len(stack) == num_courses

def dfs(node, graph, visited, stack):
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(neighbor, graph, visited, stack)
    stack.append(node)