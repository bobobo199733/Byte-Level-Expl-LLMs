def decode_string(s):
    result, stack = ('', [])
    for char in s:
        if char.isdigit():
            count = int(char)
            stack.append(count)
        elif char == '[':
            stack.append(char)
        elif char == ']':
            while stack and stack[-1] != '[':
                count = stack.pop()
                result += chr(ord(result[-1]) * count)
            stack.pop()
        elif char.isalpha():
            result += char
    while stack:
        if stack[-1] == '[':
            raise ValueError('Error in input string')
        count = stack.pop()
        for _ in range(count):
            result += chr(ord(result[-1]) * count)
    return result