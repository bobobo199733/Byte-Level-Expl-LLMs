def generate_parentheses(n):
    result = []

    def backtrack(openings, closings, max_openings=n, output=[]):
        if len(output) == 2 * n:
            result.append(''.join(output))
            return
        if openings < max_openings:
            backtrack(openings + 1, closings, max_openings, output + ['('])
        if openings > closings:
            backtrack(openings, closings + 1, max_openings, output + [')'])
    backtrack(0, 0)
    return result