def json_validator(text):
    if text == '{}' or (text[0] == '[' and text[-1] == ']'):
        for char in text[1:-1]:
            if (char == '{' or char == '[') and text.count(char) > 1:
                return False
            elif char not in ',}]' and char != ' ' and (char != '\n'):
                nested = False
                for subchar in text[char:]:
                    if subchar == '{' or subchar == '[':
                        nested = True
                        break
                    elif subchar == char and (not nested):
                        return False
                if not nested:
                    continue
            elif char == '"' and text.count(char) % 2 != 0:
                return False
    else:
        return False
    return True