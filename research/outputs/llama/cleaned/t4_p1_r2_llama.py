def decode_string(s: str) -> str:
    """
    Decodes an encoded string where numbers followed by brackets indicate repetition.

    Args:
        s (str): The encoded string to be decoded.

    Returns:
        str: The decoded string.

    Raises:
        ValueError: If the input string is invalid.
    """
    stack = []
    curr_num = 0
    curr_str = ''
    for char in s:
        if char.isdigit():
            curr_num = curr_num * 10 + int(char)
        elif char == '[':
            stack.append(curr_str)
            stack.append(curr_num)
            curr_str = ''
            curr_num = 0
        elif char == ']':
            num = stack.pop()
            prev_str = stack.pop()
            curr_str = prev_str + num * curr_str
        else:
            curr_str += char
    if stack:
        raise ValueError('Invalid input string')
    return curr_str