def json_validator(text):
    """
    Validates whether a string contains syntactically valid JSON.

    Args:
        text (str): A string containing JSON data.

    Returns:
        bool: True if the string is valid JSON, False otherwise.
    """
    text = text.strip()
    stack = []
    in_quote = False
    has_invalid_char = False
    i = 0
    while i < len(text):
        if text[i] == '"' and (not in_quote):
            stack.append('"')
            in_quote = True
        elif text[i] == '"' and in_quote:
            if len(stack) > 0 and stack[-1] == '"':
                stack.pop()
                in_quote = False
        elif text[i] == '{' or text[i] == '[':
            stack.append(text[i])
        elif text[i] == '}' or text[i] == ']':
            if len(stack) < 1:
                has_invalid_char = True
                break
            else:
                opening_bracket = stack.pop()
                if text[i] == '}' and opening_bracket != '{' or (text[i] == ']' and opening_bracket != '['):
                    has_invalid_char = True
                    break
        elif text[i] in ',:;':
            if not in_quote:
                has_invalid_char = True
                break
        if (text[i] == ',' or text[i] == '{' or text[i] == '[') and in_quote:
            has_invalid_char = True
            break
        elif (text[i] == '}' or text[i] == ']') and (not in_quote):
            has_invalid_char = True
            break
        i += 1
    if len(stack) > 0 or has_invalid_char:
        return False
    return True