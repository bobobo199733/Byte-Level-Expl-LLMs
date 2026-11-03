def is_balanced(s: str) -> bool:
    """
    Checks if the brackets in the string are balanced and properly nested.
    
    Args:
        s (str): The input string to check for bracket balance.
    
    Returns:
        bool: True if the brackets are balanced, False otherwise.
    """
    bracket_map = {')': '(', '}': '{', ']': '['}
    opening_brackets = []
    for char in s:
        if char in bracket_map.values():
            opening_brackets.append(char)
        elif char in bracket_map.keys():
            if not opening_brackets or opening_brackets.pop() != bracket_map[char]:
                return False
    return not opening_brackets