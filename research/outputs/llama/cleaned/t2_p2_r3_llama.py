def is_balanced(s: str) -> bool:
    """
    Checks whether brackets are balanced and correctly nested.
    
    Args:
        s (str): Input string containing various types of brackets.
    
    Returns:
        bool: True if the brackets in the input string are balanced, False otherwise.
    """
    bracket_pairs = {')': '(', '}': '{', ']': '['}
    stack = []
    for char in s:
        if char in bracket_pairs.values():
            stack.append(char)
        elif char in bracket_pairs.keys() and stack:
            opening_bracket = stack.pop()
            if opening_bracket != bracket_pairs[char]:
                return False
    return not stack