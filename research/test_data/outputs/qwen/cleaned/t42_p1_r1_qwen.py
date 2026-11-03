def course_schedule(num_courses, prerequisites):
    # Create an adjacency list for the graph
    from collections import defaultdict

    def build_graph(num_courses, prerequisites):
        graph = defaultdict(list)
        indegree = [0] * num_courses

        for course, prerequisite in prerequisites:
            graph[prerequisite].append(course)
            indegree[course] += 1

        return graph, indegree

    # Build the graph and indegree array
    graph, indegree = build_graph(num_courses, prerequisites)

    # Stack to perform DFS
    stack = []

    # Initialize the stack with all courses that have no incoming edges (indegree == 0)
    for i in range(num_courses):
        if indegree[i] == 0:
            stack.append(i)

    count = 0

    while stack:
        course = stack.pop()
        count += 1

        for neighbor in graph[course]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                stack.append(neighbor)

    # If the number of courses completed is equal to the total number of courses, return True
    return count == num_courses

# Example usage:
print(course_schedule(2, [[1, 0]]))  # Output: True
print(course_schedule(2, [[1, 0], [0, 1]])])  # Output: False
