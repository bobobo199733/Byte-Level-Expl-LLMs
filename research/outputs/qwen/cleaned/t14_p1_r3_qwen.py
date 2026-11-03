def generate_parentheses(n):

    def backtrack(s='', left=0, right=0):
        if left == 0 and right == 0:
            result.append(s)
            return
        if left > 0:
            backtrack(s + '(', left - 1, right + 1)
        if right > 0:
            backtrack(s + ')', left, right - 1)
    result = []
    backtrack()
    return result