def is_balanced(s):
    bracket_map = {'(': ')', '[': ']', '{': '}'}
    stack = []
    for char in s:
        if char in bracket_map:
            stack.append(char)
        elif char == bracket_map[stack[-1]] and stack:
            stack.pop()
        else:
            return False
    return not stack