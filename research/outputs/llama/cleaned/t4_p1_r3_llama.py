def decode_string(s: str) -> str:
    """
    Decodes an encoded string where a number followed by brackets means repetition.
    
    Args:
        s (str): The encoded string to be decoded.
    
    Returns:
        str: The decoded string.
    
    Raises:
        ValueError: If the input string is invalid.
    """
    stack = []
    cur_num = 0
    cur_char = ''
    for i in range(len(s)):
        if s[i].isdigit():
            cur_num = cur_num * 10 + int(s[i])
        elif s[i] == '[':
            stack.append((cur_char, cur_num))
            cur_char = ''
            cur_num = 0
        elif s[i] == ']':
            if not stack:
                raise ValueError('Invalid input string')
            num_repeats, prev_char = stack.pop()
            cur_char = prev_char + num_repeats * cur_char
        elif s[i].isalpha():
            if s[i - 1] == ']':
                raise ValueError('Invalid input string')
            else:
                cur_char += s[i]
    return cur_char