def remove_k_digits(num: str, k: int) -> str:
    """
    Removes k digits from the number string so the result is as small as possible.
    
    Args:
    num (str): The input number string.
    k (int): The number of digits to be removed.
    
    Returns:
    str: The resulting number string with k digits removed.
    """
    stack = []
    for digit in num:
        while k > 0 and stack and (stack[-1] > digit):
            k -= 1
            stack.pop()
        stack.append(digit)
    while k > 0:
        stack.pop()
        k -= 1
    return ''.join(stack).lstrip('0') or '0'