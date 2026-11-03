from collections import defaultdict

def course_schedule(num_courses, prerequisites):
    graph = defaultdict(list)
    in_degree = [0] * num_courses
    for course, prereq in prerequisites:
        graph[prereq].append(course)
        in_degree[course] += 1
    zero_indegree_queue = [i for i in range(num_courses) if in_degree[i] == 0]
    from collections import deque
    queue = deque(zero_indegree_queue)
    completed_courses = 0
    while queue:
        current_course = queue.popleft()
        completed_courses += 1
        for course in graph[current_course]:
            in_degree[course] -= 1
            if in_degree[course] == 0:
                queue.append(course)
    return completed_courses == num_courses