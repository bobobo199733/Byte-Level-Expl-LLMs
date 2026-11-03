def course_schedule(num_courses, prerequisites):
    from collections import defaultdict
    adj_list = defaultdict(list)
    for pre in prerequisites:
        adj_list[pre[0]].append(pre[1])
    visited = [False] * num_courses
    processing = set()

    def is_cyclic(course):
        """
        Helper function to perform DFS and check for cycles.
        """
        if course in processing:
            return True
        if visited[course]:
            return False
        processing.add(course)
        for next_course in adj_list[course]:
            if is_cyclic(next_course):
                return True
        processing.remove(course)
        visited[course] = True
        return False
    for course in range(num_courses):
        if not visited[course]:
            if is_cyclic(course):
                return False
    return True