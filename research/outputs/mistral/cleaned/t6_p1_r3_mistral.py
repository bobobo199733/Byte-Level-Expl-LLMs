def wildcard_match(s: str, p: str) -> bool:

    def match(i, j):
        if j == len(p):
            return i == len(s)
        if j + 1 < len(p) and p[j + 1] == '*':
            return match(i, j + 1) or (i < len(s) and s[i] == p[i] or match(i + 1, j))
        if i < len(s) and (p[j] == s[i] or p[j] == '?'):
            return match(i + 1, j + 1)
        else:
            return False
    return match(0, 0)