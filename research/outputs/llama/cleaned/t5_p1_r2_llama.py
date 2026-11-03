def remove_k_digits(num: str, k: int) -> str:
    """
    Removes exactly k digits from the non-negative integer string num 
    so that the resulting number is as small as possible.

    Args:
        num (str): A non-negative integer string.
        k (int): The number of digits to remove.

    Returns:
        str: The result as a string. If the result is empty, returns "0".
    """
    stack = []
    for digit in num:
        while k > 0 and stack and (stack[-1] > digit):
            stack.pop()
            k -= 1
        stack.append(digit)
    if len(stack) == k:
        return '0'
    result = ''.join(stack).lstrip('0') or '0'
    return result