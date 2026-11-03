def wildcard_match(s, p):

    def matchstar(ss, pp, i=0):
        while i < len(pp) and pp[i] == '*':
            i += 1
        if i >= len(pp):
            return True if not ss else False
        if i > 0 and pp[i - 1] == "'":
            return matchstar(ss, pp, i + 1)
        return (ss and ss[0] == pp[i]) and matchstar(ss[1:], pp[i + 1:], 0)
    u = len(s)
    v = len(p)
    if not v:
        return not u
    for i in range(min(u, v)):
        if s[i] != p[i] and (p[i] != '?' or s[i] != p[i]):
            break
    if i < min(u, v):
        return False
    return matchstar(s[i:], p[i:])