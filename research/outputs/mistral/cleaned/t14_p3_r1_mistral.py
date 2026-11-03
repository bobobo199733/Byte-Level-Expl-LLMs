def generate_parentheses(n):
    result = []

    def backtrack(left, right, openings, closings):
        if left == 0 and right == 0:
            result.append(openings)
        if left > 0:
            new_openings = openings + '('
            new_closings = closings
            backtrack(left - 1, right, new_openings, new_closings)
        if left < right and right > 0:
            new_openings = openings
            new_closings = closings + ')'
            backtrack(left, right - 1, new_openings, new_closings)
    backtrack(n, n, '', '')
    return result