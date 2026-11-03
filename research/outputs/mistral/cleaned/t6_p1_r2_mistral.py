def wildcard_match(s: str, p: str) -> bool:

    def match(s_, p_):
        if not p_:
            return not s_
        first = s_ and p_[0] in {'*', '?'}
        if len(p_) > 1 and p_[1] == '$':
            return match(s_, p_[2:])
        if first:
            return match(s[1:], p_[1:]) or (not s_ and match(s, p[1:]))
        if s_ and p_[0] == s[0]:
            return match(s[1:], p[1:])
        return False
    return match(s, p)