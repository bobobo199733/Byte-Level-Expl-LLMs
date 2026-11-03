def json_validator(text):

    def valid_char(c):
        return c in '{},[]()\n:\x0c\r\t\\"' or (c.startswith('u') and len(c) == 6 and (c[2:] in hex(ord(c[4]))[2:]))
    if not text:
        return False
    stack = []
    for char in text:
        if char == '{' or char == '[':
            stack.append(char)
        elif char == '}' or char == ']':
            if not stack or stack.pop() != char:
                return False
        elif char == '"' and (not stack or stack[-1] != '\\'):
            if not text[text.index(char) - 1] == '\\':
                return False
        elif not valid_char(char):
            return False
    return not stack