def remove_k_digits(num: str, k: int) -> str:
    """
    Removes exactly k digits from the non-negative integer string num so that 
    the resulting number is as small as possible.

    Args:
        num (str): The input integer string.
        k (int): The number of digits to remove.

    Returns:
        str: The resulting number as a string, with leading zeros removed. If the result is empty, returns "0".
    """
    if k == 0 or k >= len(num):
        return num
    stack = []
    for n in num:
        while stack and stack[-1] > n and k:
            stack.pop()
            k -= 1
        stack.append(n)
    if k:
        stack = stack[:-k]
    res = ''.join(stack).lstrip('0') or '0'
    return res