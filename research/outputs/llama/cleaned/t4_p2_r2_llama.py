def decode_string(s: str) -> str:
    """
    Decodes a string with nested patterns into its plain text representation.
    
    Args:
        s (str): The input string to be decoded.
    
    Returns:
        str: The decoded string.
    """
    stack = []
    res = ''
    curr_num = 0
    curr_str = ''
    for c in s:
        if c.isdigit():
            curr_num = curr_num * 10 + int(c)
        elif c == '[':
            stack.append(curr_str)
            stack.append(curr_num)
            curr_str = ''
            curr_num = 0
        elif c == ']':
            num = stack.pop()
            prev_str = stack.pop()
            curr_str = prev_str + num * curr_str
        else:
            curr_str += c
    return res + curr_str