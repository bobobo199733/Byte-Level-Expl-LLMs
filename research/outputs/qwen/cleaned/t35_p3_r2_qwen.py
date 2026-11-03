def json_validator(text):

    def parse_value(value, stack=None):
        if value.startswith('{') or value.startswith('['):
            return parse_container(value, stack)
        else:
            return parse_string_or_number(value)

    def parse_container(container, stack):
        level = 1
        index = 0
        while index < len(container) - 1:
            if container[index] == ',' and stack[-1][1] in ('[', '{'):
                return (False, 'Unexpected comma')
            elif container[index:index + 2] == ': ':
                key = parse_string(container[index + 2:])
                value = parse_value(key)
                stack.append((key, value))
            elif container[index] in [']', '}']:
                level -= 1
                if level < 0:
                    return (False, 'Unmatched closing bracket')
                else:
                    index += 1
                    continue
            index += 1
        if len(stack) == 1 and (not isinstance(stack[0][1], (dict, list))):
            return stack[0]
        return (False, 'Incomplete container')

    def parse_string(string):
        level = 0
        start = None
        for i, char in enumerate(string):
            if char == '"' and (not level or string[i - 1] != '\\'):
                if not start:
                    start = i + 1
                else:
                    return string[start:i].strip()
            elif char in ['"', '\n']:
                continue
            elif char == '\\' and string[i - 1] != '\\':
                continue
            level += (char == '"') - (char == '"')
        return (False, 'Invalid string')

    def parse_string_or_number(string):
        if string[0].isdigit() or string[0] in ['-', '+']:
            try:
                value = eval(string)
                if isinstance(value, (int, float)):
                    return value
            except Exception:
                pass
        return (False, 'Invalid number')
    text = text.strip()
    if not text:
        return False
    parsed_data, error = parse_value(text)
    if not error:
        return True
    return f'JSON validation failed: {error}'