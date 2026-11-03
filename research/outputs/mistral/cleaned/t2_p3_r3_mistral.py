def is_balanced(s: str) -> bool:
    brackets = {')': '(', ']': '[', '}': '{'}
    stack = []
    for char in s:
        if char in brackets:
            if not stack or stack.pop() != brackets[char]:
                return False
        else:
            stack.append(char)
    return len(stack) == 0