def generate_parentheses(n):

    def backtrack(s='', left=0, right=0):
        if len(s) == 2 * n:
            combinations.append(s)
            return
        if left < n:
            backtrack(s + '(', left + 1, right)
        if right < left:
            backtrack(s + ')', left, right + 1)
    combinations = []
    backtrack()
    return combinations