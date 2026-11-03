def wildcard_match(s: str, p: str) -> bool:

    def match(i, j):
        if not j:
            return not i
        if j == '*':
            return match(i, p[1:]) or (not i and match(0, p))
        return i == j or j == '?'
    return match(s, p)