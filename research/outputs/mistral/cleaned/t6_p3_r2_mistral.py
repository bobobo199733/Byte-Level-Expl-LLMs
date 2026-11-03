def wildcard_match(s, p):

    def match(s, m):
        if not s:
            return not m
        if not m:
            return False
        last_m = m and m[-1] != '*'
        if last_m:
            return s[0] == m[0] and match(s[1:], m[1:])
        else:
            return any((match(s[i:], m) for i in range(len(s) + 1)))
    return match(s, p)