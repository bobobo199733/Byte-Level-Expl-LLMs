import collections

def dfs(graph, visited, recursive_visited, course):
    visited[course] = True
    recursive_visited[course] = True
    for neighbor in graph[course]:
        if not visited[neighbor] and (not recursive_visits[neighbor]):
            dfs(graph, visited, recursive_visited, neighbor)
        elif recursive_visited[neighbor]:
            raise ValueError('Cyclic dependency detected')
    recursive_visited[course] = False

def topological_sort(graph):
    n = len(graph)
    visited = [False] * n
    recursive_visits = [False] * n
    order = []
    for course in range(n):
        if not visited[course]:
            dfs(graph, visited, recursive_visits, course)
            order.append(course)
    return order if len(order) == n else None

def course_schedule(num_courses, prerequisites):
    graph = collections.defaultdict(list)
    for pair in prerequisites:
        graph[pair[1]].append(pair[0])
    if not topological_sort(graph):
        raise ValueError('There is no solution')
    return len(topological_sort(graph)) == num_courses