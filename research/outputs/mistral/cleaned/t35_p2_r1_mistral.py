def json_validator(text):
    valid_characters = set('{},[]: \t\n\x0c\r0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-._')
    opening_brackets = '([{'
    closing_brackets = ')]}'
    stack = []
    for char in text:
        if char == "'" or char == '"':
            if stack and stack[-1] != '\\':
                last_char = stack.pop()
                if last_char != char:
                    return False
            else:
                stack.append(char)
        elif char in opening_brackets + '\\':
            stack.append(char)
        elif char in closing_brackets:
            if not stack or (stack and stack[-1] != char[1] and (char != '\\') or not stack[-1] == '\\'):
                return False
            elif char == ']' and stack and (stack[-1] == '{'):
                return False
            else:
                stack.pop()
        elif char in valid_characters - opening_brackets - closing_brackets - '\\':
            pass
        else:
            return False
    return not stack