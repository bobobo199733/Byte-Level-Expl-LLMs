def is_balanced(s):
    brackets = {')': '(', ']': '[', '}': '{'}
    stack = []
    for char in s:
        if char in brackets.values():
            stack.append(char)
        elif char in brackets and len(stack) > 0 and (brackets[char] == stack[-1]):
            stack.pop()
        else:
            return False
    return len(stack) == 0