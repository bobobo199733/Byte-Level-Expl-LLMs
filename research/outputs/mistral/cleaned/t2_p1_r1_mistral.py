def is_balanced(s):
    brackets = {')': '(', ']': '[', '}': '{'}
    bracket_map = {'(': 1, '[': 2, '{}': 3}
    stack = []
    for char in s:
        if char in brackets:
            top_char = stack.pop() if stack else None
            if not top_char or brackets[top_char] != char:
                return False
        elif char in bracket_map:
            stack.append(bracket_map[char])
    return not stack