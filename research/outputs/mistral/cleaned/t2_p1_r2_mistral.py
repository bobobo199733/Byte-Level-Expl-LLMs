def is_balanced(s):
    brackets = {')': '(', ']': '[', '}': '{'}
    stack = []
    for char in s:
        if char in brackets.values():
            stack.append(char)
        elif char in brackets and (not stack) or brackets[char] != stack[-1]:
            return False
        elif char in brackets:
            stack_top = stack.pop() if stack else '#'
            if brackets[char] != stack_top:
                return False
    return not stack