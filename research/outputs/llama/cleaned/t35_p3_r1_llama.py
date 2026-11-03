def json_validator(text):
    """
    Validates if a given string is a valid JSON representation.

    :param text: The string to be validated as JSON.
    :return: `True` if the string is a valid JSON, `False` otherwise.
    """
    stack = []
    for char in text:
        if char == '{' or char == '[':
            if stack and stack[-1] in ['{', '[']:
                return False
            stack.append(char)
        elif char == '}' or char == ']':
            if not stack:
                return False
            top = stack.pop()
            if top == '{' and char != '}' or (top == '[' and char != ']'):
                return False
        elif char in [',', ':']:
            continue
    if stack:
        return False
    return True