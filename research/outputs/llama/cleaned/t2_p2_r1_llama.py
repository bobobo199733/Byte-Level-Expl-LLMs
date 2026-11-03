def is_balanced(s: str) -> bool:
    """
    Check whether brackets are balanced and correctly nested.

    Args:
        s (str): The input string containing brackets.

    Returns:
        bool: True if brackets are balanced, False otherwise.
    """
    bracket_map = {')': '(', '}': '{', ']': '['}
    stack = []
    for char in s:
        if char in bracket_map.values():
            stack.append(char)
        elif char in bracket_map.keys():
            if not stack or stack.pop() != bracket_map[char]:
                return False
    return not stack