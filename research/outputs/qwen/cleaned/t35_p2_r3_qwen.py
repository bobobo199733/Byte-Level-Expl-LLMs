def json_validator(text):
    stack = []
    bracket_map = {')': '(', '}': '{', ']': '['}
    valid_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-+.,:/\'"{}[]!@#$%^&*()_<>? ')

    def is_valid_char(c):
        return c in valid_chars or ord(c) >= 128
    i = 0
    while i < len(text):
        if not is_valid_char(text[i]):
            return False
        if text[i] == '"' or text[i] == "'":
            start = i
            i += 1
            while i < len(text) and text[i] != text[start]:
                if not is_valid_char(text[i]):
                    return False
                i += 1
            if i >= len(text):
                return False
        elif text[i] in '{[(':
            stack.append(text[i])
        elif text[i] in '}])':
            if not stack or stack[-1] == bracket_map[text[i]]:
                stack.pop()
            else:
                return False
        i += 1
    return len(stack) == 0