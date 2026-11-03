def is_balanced(s: str) -> bool:
    bracket_map = {')': '(', ']': '[', '}': '{'}
    open_brackets = set(bracket_map.values())
    stack = []
    for char in s:
        if char in open_brackets:
            stack.append(char)
        elif char in bracket_map:
            if not stack or stack.pop() != bracket_map[char]:
                return False
    return len(stack) == 0