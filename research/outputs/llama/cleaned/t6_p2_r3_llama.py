def wildcard_match(s: str, p: str) -> bool:
    """
    Check whether a string matches a wildcard pattern.

    Args:
        s (str): The input string.
        p (str): The wildcard pattern where '?' matches one character and '*' matches any sequence of characters.

    Returns:
        bool: True if the string matches the pattern, False otherwise.
    """
    s_ptr = 0
    p_ptr = 0
    while p_ptr < len(p):
        if p[p_ptr] == '*':
            p_ptr += 1
            while p_ptr < len(p) and p[p_ptr] != '*':
                p_ptr += 1
            if p_ptr == len(p):
                break
            s_ptr = skip_chars(s, s_ptr)
        elif p[p_ptr] == '?':
            s_ptr += 1
            p_ptr += 1
        else:
            p_ptr = skip_pattern(s, s_ptr, p_ptr)
            break
    while s_ptr < len(s) and p_ptr < len(p):
        if not (p[p_ptr] == '?' or p[p_ptr] == '*'):
            return False
        s_ptr += 1
        p_ptr += 1
    return True

def skip_chars(s: str, s_ptr: int) -> int:
    """
    Skip any sequence of characters in the string and move forward one step.

    Args:
        s (str): The input string.
        s_ptr (int): The current pointer position in the string.

    Returns:
        int: The new pointer position after skipping any sequence of characters.
    """
    while s_ptr < len(s) and s[s_ptr] != '*':
        s_ptr += 1
    return s_ptr

def skip_pattern(s: str, s_ptr: int, p_ptr: int) -> int:
    """
    Skip the '*' in the pattern and move forward one step.

    Args:
        s (str): The input string.
        s_ptr (int): The current pointer position in the string.
        p_ptr (int): The current pointer position in the pattern.

    Returns:
        int: The new pointer position after skipping the '*'.
    """
    while p_ptr < len(p) and p[p_ptr] == '*':
        if p_ptr + 1 < len(p) and p[p_ptr + 1] != '*':
            return s_ptr
        p_ptr += 2
    return p_ptr