def generate_parentheses(n):
    res = []

    def backtrack(left=0, right=0, open_parens=n, closed_parens=n, result=''):
        if left == open_parens and right == closed_parens:
            res.append(result)
            return
        if open_parens > left:
            backtrack(left + 1, right, open_parens, closed_parens, result + '(')
        if closed_parens > right and right < open_parens:
            backtrack(left, right + 1, open_parens, closed_parens, result + ')')
    backtrack()
    return res