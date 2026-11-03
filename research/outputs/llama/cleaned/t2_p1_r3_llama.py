def is_balanced(s: str) -> bool:
    """
    Return True if the brackets in the string are balanced and properly nested, 
    and False otherwise.
    
    :param s: Input string to check for bracket balance
    :return: bool indicating whether brackets are balanced
    """
    bracket_map = {')': '(', ']': '[', '}': '{'}
    stack = []
    for char in s:
        if char not in bracket_map and char not in ['(', '[', '{']:
            continue
        if char in ['(', '[', '{']:
            stack.append(char)
        elif char in [')', ']', '}']:
            if not stack or stack.pop() != bracket_map[char]:
                return False
    return not stack