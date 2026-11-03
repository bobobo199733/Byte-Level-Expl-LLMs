def remove_k_digits(num: str, k: int) -> str:
    """
    Removes k digits from the number string so the result is as small as possible.

    Args:
        num (str): The input number string.
        k (int): The number of digits to be removed.

    Returns:
        str: The smallest possible resulting number after removing k digits.
    """
    stack = []
    for digit in num:
        while stack and stack[-1] > digit and k:
            stack.pop()
            k -= 1
        stack.append(digit)
    if k:
        stack = stack[:-k]
    return ''.join(stack).lstrip('0') or '0'