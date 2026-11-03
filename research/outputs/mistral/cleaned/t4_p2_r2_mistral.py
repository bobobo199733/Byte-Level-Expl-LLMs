def decode_string(s):
    result = ''
    i = 0
    while i < len(s):
        count = 1
        if i + 1 < len(s) and s[i] == '[':
            i += 1
            multiplier = ''
            while i + 1 < len(s) and s[i] != ']':
                if s[i] == '[':
                    multiplier += decode_string(s[i])
                elif s[i].isdigit():
                    multiplier += s[i]
                i += 1
            count *= int(multiplier)
        result += count * s[i + 1] if i + 1 < len(s) and (not s[i] == '[') else s[i]
        i += 1
    return result