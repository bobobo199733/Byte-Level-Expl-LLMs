def wildcard_match(s, p):

    def match(i, j):
        if not p:
            return not s
        first_match = bool(s) and (p[0] == s[0] or p[0] == '?')
        if len(p) > 1 and p[1] == '*':
            return match(i, j - 1) or (first_match and match(i + 1, j))
        else:
            return first_match and match(i + 1, j)
    return match(0, len(p))