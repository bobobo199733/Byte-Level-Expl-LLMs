def json_validator(text):
    if not text or (text[0] != '{' and text[-1] != '}'):
        return False

    def validate(index, current=None, stack=[], allow_array=True):
        if index == len(text):
            return bool(current) and (not stack)
        char = text[index]
        if char.isspace():
            return validate(index + 1, current, stack)
        if char in ['{', '[']:
            stack.append(char)
            return validate(index + 1, char, stack, allow_array and char == '[')
        if char in [']', '}']:
            expected = stack.pop()
            if char != expected or (stack and stack[-1] != '['):
                return False
            if not stack:
                return validate(index + 1, None)
        if char in ['f', 't', 'n', 'r']:
            current = char.lower() == char
            return validate(index + 1, current, stack)
        if char.isdigit():
            is_number = True
            while index < len(text) and text[index].isdigit():
                index += 1
            if index < len(text):
                point_index = text.find('.', index)
                exponent_index = text.find('e', index)
                if point_index != -1 and (exponent_index == -1 or point_index < exponent_index):
                    index = point_index + 1
                elif exponent_index != -1:
                    index = exponent_index
                else:
                    is_number = False
            if not is_number:
                return False
            if validate(index, float(text[:index]), stack):
                return True
        if char == '"':
            if not current or not (isinstance(current, str) and len(current)):
                return False
            escaped = False
            i = index + 1
            while i < len(text):
                next_char = text[i]
                if next_char == '\\' and i + 1 < len(text) and (text[i + 1] == 'u' or text[i + 1] in ['\\",{}[]']):
                    i += 2
                elif next_char != '"':
                    i += 1
                else:
                    break
            if i != index + 2:
                return validate(i, current + text[index + 1:i], stack)
        return False
    return validate(0)