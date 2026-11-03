def json_validator(text):
    valid_chars = set('[]{}:,"<> \t\n\r\x0b\x0c\x08-0123456789. ')

    def is_unquoted_char(c):
        return c.isalnum() or c in '-+@*#%&^?|<>=~!,;:(){}[]<>'
    stack = []
    last_char = None
    for char in text:
        if char == '"':
            if not stack and (last_char is None or last_char != '\\'):
                return False
            elif stack and stack[-1] != '\\':
                stack.pop()
        elif char in '{[,':
            stack.append(char)
        elif char in '}]':
            if not stack or (char == '}' and stack[-1] != '{') or (char == ']' and stack[-1] != '['):
                return False
            stack.pop()
        elif last_char is None:
            continue
        elif char in valid_chars and (not is_unquoted_char(char)):
            return False
        last_char = char
    return len(stack) == 0