def generate_parentheses(n):
    result = []

    def backtrack(left, right, output):
        if left == right and left == n:
            result.append(output)
        if left > n or right > left:
            return
        backtrack(left + 1, right, output + '(')
        if left > 0:
            backtrack(left, right + 1, output + ')')
    backtrack(0, 0, '')
    return result