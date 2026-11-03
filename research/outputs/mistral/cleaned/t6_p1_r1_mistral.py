def wildcard_match(s, p):

    def match_helper(s, p, i=0, j=0):
        if j == len(p):
            return i == len(s)
        if p[j] == '*':
            while i < len(s) and (j + 1 < len(p) and p[j + 1] == '*'):
                j += 1
            if j >= len(p):
                return match_helper(s, p, i, j - 1)
            else:
                return match_helper(s, p, i) or match_helper(s[i + 1:], p, i + 1, j)
        if p[j] == '?' or s[i] == p[j]:
            return match_helper(s, p, i + 1, j + 1)
        return False
    return match_helper(s, p)