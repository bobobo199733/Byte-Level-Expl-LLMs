def is_balanced(s: str) -> bool:
    bracket_map = {')': '(', ']': '[', '}': '{'}
    stack = []
    for char in s:
        if char in bracket_map.values():
            stack.append(char)
        elif char in bracket_map.keys():
            if not stack or stack.pop() != bracket_map[char]:
                return False
        else:
            continue
    return len(stack) == 0