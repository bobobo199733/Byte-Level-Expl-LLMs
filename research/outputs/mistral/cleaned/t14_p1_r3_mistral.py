def generate_parentheses(n):
    result = []

    def backtrack(left, right, output):
        if left == n and right == n:
            result.append(output)
        if left > 0 and right < left:
            backtrack(left - 1, right + 1, output + '(')
            backtrack(left, right, output + ')')
        if left > right:
            return
        backtrack(left, right, output)
    backtrack(n, 0, '')
    return result