from collections import defaultdict, deque

def canFinish(num_courses, prerequisites):
    graph = defaultdict(list)
    for course, prereq in prerequisites:
        graph[prereq].append(course)
    visited = set()
    stack = deque()

    def dfs(course):
        if course in visited:
            return False
        if course in graph and any((dfs(prereq) for prereq in graph[course])):
            return False
        visited.add(course)
        stack.append(course)
        for prereq in graph[course]:
            dfs(prereq)
        if not stack:
            return True
        current = stack.pop()
        visited.remove(current)
        return True
    if not dfs(0):
        return False
    return len(visited) == num_courses