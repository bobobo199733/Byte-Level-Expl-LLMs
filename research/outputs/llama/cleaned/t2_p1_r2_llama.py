def is_balanced(s: str) -> bool:
    """
    Returns True if the brackets in the string are balanced and properly nested, False otherwise.
    
    :param s: input string to check for balanced brackets
    :return: boolean indicating whether brackets are balanced
    """
    bracket_map = {')': '(', '}': '{', ']': '['}
    opening_brackets = []
    for char in s:
        if not (char in bracket_map.keys() or char in ['(', '[', '{']):
            continue
        elif char in ['(', '[', '{']:
            opening_brackets.append(char)
        elif not opening_brackets or opening_brackets.pop() != bracket_map[char]:
            return False
    return not opening_brackets