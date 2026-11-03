def generate_parentheses(n):
    result = []

    def backtrack(left, right, paren=''):
        if left == right and left == n:
            result.append(paren)
        if left > 0:
            backtrack(left - 1, right, paren + '(')
        if left < right:
            backtrack(left, right + 1, paren + ')')
    backtrack(n, 0, '')
    return result