def is_balanced(s: str) -> bool:
    """
    Check whether brackets are balanced and correctly nested.

    Args:
        s (str): The input string containing brackets and possibly other characters.

    Returns:
        bool: True if the brackets in the string are balanced, False otherwise.
    """
    bracket_map = {')': '(', '}': '{', ']': '['}
    stack = []
    for char in s:
        if char in bracket_map.values():
            stack.append(char)
        elif char in bracket_map.keys() and stack:
            last_opening = stack.pop()
            if bracket_map[char] != last_opening:
                return False
    return not stack