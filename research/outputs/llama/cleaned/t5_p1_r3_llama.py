def remove_k_digits(num: str, k: int) -> str:
    """
    Removes exactly k digits from the non-negative integer string num so 
    that the resulting number is as small as possible.

    Args:
        num (str): A non-negative integer string.
        k (int): The number of digits to remove.

    Returns:
        str: The result as a string, with leading zeros removed. If the result is empty, returns "0".
    """
    num = list(num)
    if k == len(num):
        return '0'
    stack = []
    for i, digit in enumerate(num):
        while k > 0 and stack and (stack[-1] > digit):
            k -= 1
            stack.pop()
        stack.append(digit)
    if k > 0:
        stack = stack[:-k]
    result = ''.join(stack).lstrip('0')
    return result if result else '0'