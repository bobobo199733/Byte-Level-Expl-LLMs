def generate_parentheses(n):
    result = []

    def backtrack(left, right, string=''):
        if left == right and left == n:
            result.append(string)
        if left > n or right > left:
            return
        backtrack(left + 1, right, string + '(')
        backtrack(left, right + 1, string + ')')
    backtrack(0, 0)
    return result