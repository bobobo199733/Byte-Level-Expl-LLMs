def decode_string(s: str) -> str:
    """
    Decodes an encoded string.

    Args:
        s (str): The encoded string to be decoded.

    Returns:
        str: The decoded string.

    Raises:
        ValueError: If the input is invalid.
    """
    stack = []
    num = 0
    res = ''
    for c in s:
        if c.isdigit():
            num = num * 10 + int(c)
        elif c == '[':
            stack.append(res)
            res = ''
            stack.append(num)
            num = 0
        elif c == ']':
            count = stack.pop()
            prev_str = stack.pop()
            res = prev_str + count * res
        else:
            res += c
    return res