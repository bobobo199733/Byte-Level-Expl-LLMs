def wildcard_match(s: str, p: str) -> bool:

    def match(i: int, j: int) -> bool:
        if j == len(p):
            return i == len(s)
        first_match = i < len(s) and (p[j] == s[i] or p[j] == '?')
        if p[j] == '*':
            return match(i, j + 1) or (i < len(s) and match(i + 1, j))
        else:
            return first_match and match(i + 1, j + 1)
    return match(0, 0)