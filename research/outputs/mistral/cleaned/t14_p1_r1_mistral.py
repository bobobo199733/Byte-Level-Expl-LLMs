def generate_parentheses(n):
    result = []

    def backtrack(open_count=0, close_count=0, remaining=n * 2):
        if open_count > n or close_count > n or close_count > open_count:
            return
        if open_count == n and close_count == n:
            result.append('('.join(')' * close_count + '(' * open_count) + ')')
            return
        if remaining > 0:
            backtrack(open_count + 1, close_count, remaining - 2)
            if open_count > 0:
                backtrack(open_count, close_count + 1, remaining)
    backtrack()
    return result