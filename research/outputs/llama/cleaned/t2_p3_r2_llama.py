def is_balanced(s: str) -> bool:
    stack = []
    brackets_map = {')': '(', '}': '{', ']': '['}
    for char in s:
        if char in brackets_map.values():
            stack.append(char)
        elif char in brackets_map.keys():
            if not stack or stack.pop() != brackets_map[char]:
                return False
    return True