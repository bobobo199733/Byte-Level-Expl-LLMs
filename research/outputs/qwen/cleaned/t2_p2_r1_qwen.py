def is_balanced(s: str) -> bool:
    bracket_pairs = {')': '(', ']': '[', '}': '{'}
    stack = []
    for char in s:
        if char in bracket_pairs.values():
            stack.append(char)
        elif char in bracket_pairs.keys():
            if not stack or stack[-1] != bracket_pairs[char]:
                return False
            stack.pop()
    return len(stack) == 0