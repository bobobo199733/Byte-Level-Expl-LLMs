from collections import defaultdict, deque

def course_schedule(num_courses: int, prerequisites: list[list[int]]) -> bool:
    """
    Determines whether all courses can be completed.

    Args:
        num_courses (int): Number of courses.
        prerequisites (list[list[int]]): Prerequisite pairs where [a, b] means course a depends on course b.

    Returns:
        bool: True if all courses can be completed, otherwise False.
    """
    graph = defaultdict(list)
    for course, prerequisite in prerequisites:
        graph[prerequisite].append(course)
    visited = set()
    recursion_stack = set()

    def dfs(course: int) -> bool:
        """
        Performs depth-first search to detect cycles.

        Args:
            course (int): Current course.

        Returns:
            bool: True if no cycle detected, otherwise False.
        """
        if course in recursion_stack:
            return False
        visited.add(course)
        recursion_stack.add(course)
        for neighbor in graph[course]:
            if neighbor not in visited or dfs(neighbor):
                return True
        recursion_stack.remove(course)
        return False
    for course in range(num_courses):
        if course not in visited and (not dfs(course)):
            return False
    return True