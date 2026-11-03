def wildcard_match(s, p):

    def match(s, m):
        if not s and (not m):
            return True
        if not s or not m:
            return False
        if m[0] == '*':
            return match(s, m[1:])
        elif m[0] == '?' or m[0] == s[0]:
            return match(s[1:], m[1:]) if m else True
        return False
    return match(s, p)