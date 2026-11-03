def is_balanced(s):
    brackets = {')': '(', '}': '{', ']': '['}
    stack = []
    for char in s:
        if char in brackets.values() or not stack:
            stack.append(char)
        elif char in brackets and stack and (brackets[char] == stack[-1]):
            stack.pop()
        else:
            return False
    return not stack