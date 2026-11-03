def wildcard_match(s, p):

    def match(s_index, p_index):
        if p_index == len(p):
            return s_index == len(s)
        current_char = p[p_index]
        next_char = None
        if current_char == '*':
            if match(s_index, p_index + 1):
                return True
            while s_index < len(s):
                if match(s_index + 1, p_index):
                    return True
                s_index += 1
            return False
        elif current_char == '?' or (current_char == s[s_index] and next_char is None):
            if p_index + 1 < len(p) and p[p_index + 1] == '*':
                return match(s_index + 1, p_index + 2)
            if p_index + 1 < len(p) and p[p_index + 1] != s[s_index + 1]:
                return False
            if s_index < len(s) - 1 and match(s_index + 1, p_index + 1):
                return True
        else:
            return False
    return match(0, 0)