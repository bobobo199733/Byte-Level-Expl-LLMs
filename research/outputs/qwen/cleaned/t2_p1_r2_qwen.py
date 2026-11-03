def is_balanced(s: str) -> bool:
    bracket_pairs = {')': '(', ']': '[', '}': '{'}
    stack = []
    for char in s:
        if char in bracket_pairs.values():
            stack.append(char)
        elif char in bracket_pairs:
            if not stack or stack.pop() != bracket_pairs[char]:
                return False
    return len(stack) == 0