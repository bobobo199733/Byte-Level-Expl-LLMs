def generate_parentheses(n):
    result = []

    def backtrack(left, right, openings):
        if left == n and right == n:
            result.append(openings)
        elif left > n or right > n:
            return
        else:
            backtrack(left + 1, right, openings + '(')
            backtrack(left, right + 1, openings + ')')
    backtrack(0, 0, '')
    return result