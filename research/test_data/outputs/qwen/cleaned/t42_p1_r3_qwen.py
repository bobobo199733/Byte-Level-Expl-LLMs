def course_schedule(num_courses, prerequisites):
    graph = [[] for _ in range(num_courses)]
    for course, prereq in prerequisites:
        graph[prereq].append(course)

    def dfs(course):
        if visited[course] == 'in_progress':
            return False
        if visited[course] == 'completed':
            return True
        visited[course] = 'in_progress'
        for next_course in graph[course]:
            if not dfs(next_course):
                return False
        visited[course] = 'completed'
        return True
    visited = ['unvisited'] * num_courses
    for i in range(num_courses):
        if visited[i] == 'unvisited' and (not dfs(i)):
            return False
    return True