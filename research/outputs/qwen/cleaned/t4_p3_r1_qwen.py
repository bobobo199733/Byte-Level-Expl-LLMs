def decode_string(s: str) -> str:
    if not s:
        raise ValueError('Empty string')
    stack, num, word = ([], 0, '')
    for char in s:
        if char.isdigit():
            num = num * 10 + int(char)
        elif char.isalpha():
            word += char
        elif char == '[':
            stack.append((word, num))
            word, num = ('', 0)
        elif char == ']':
            prev_word, prev_num = stack.pop()
            word = prev_word + prev_num * word
    return word if not stack else ''