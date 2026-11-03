def is_valid(char, value=None):
    if char == '{':
        stack = []
        return True
    if char == '}':
        if not stack or stack[-1] != '{':
            return False
        stack.pop()
        return len(stack) == 0
    if char in ',[]{}':
        if not stack:
            return False
        return True
    if char == ':' and value is None:
        return False
    if char == '"' and (value is not None and isinstance(value, str)):
        return True
    if char in '{},[]' and (not stack):
        return False
    if char != ',':
        if value is None or not isinstance(value, str):
            return False
    if stack and stack[-1] == '[':
        if not (isinstance(value, list) or isinstance(value, int) or isinstance(value, float)):
            return False
        return True
    if stack and stack[-1] == '{':
        if not (isinstance(value, dict) or isinstance(value, str) or isinstance(value, int) or isinstance(value, float)):
            return False
        return True
    if value is not None:
        stack.append(char)
    return is_valid(char[1], char[0] if char[0] == '\\' else char[1])

def json_validator(text):
    if text[0] != '{' and text[-1] != '}':
        return False
    if not text:
        return True
    stack = [None]
    for char in text[1:-1]:
        if not is_valid(char, stack[-1]):
            return False
        stack.append(char)
    return len(stack) == 0