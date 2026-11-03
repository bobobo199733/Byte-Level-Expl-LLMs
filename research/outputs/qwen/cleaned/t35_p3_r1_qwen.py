def json_validator(text):
    if not (text.startswith('{') and text.endswith('}')):
        return False
    stack = []
    key_mode = False
    for i, char in enumerate(text):
        if char == '"':
            key_mode = not key_mode
        elif char == '{' and (not key_mode):
            stack.append('{')
        elif char == '}' and (not key_mode):
            try:
                stack.pop()
            except IndexError:
                return False
    return len(stack) == 0