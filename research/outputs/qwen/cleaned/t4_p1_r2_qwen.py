def decode_string(s: str) -> str:
    stack = []
    current_number = 0
    current_string = ''
    for char in s:
        if char.isdigit():
            current_number = current_number * 10 + int(char)
        elif char.isalpha():
            current_string += char
        elif char == '[':
            stack.append((current_string, current_number))
            current_string = ''
            current_number = 0
        elif char == ']':
            prev_string, num = stack.pop()
            current_string = prev_string + num * current_string
    return current_string