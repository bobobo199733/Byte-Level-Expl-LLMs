from collections import deque

def remove_k_digits(num: str, k: int) -> str:
    """
    Remove k digits from the number string so the result is as small as possible.

    Args:
        num (str): The input number as a string.
        k (int): The number of digits to be removed.

    Returns:
        str: The smallest possible number after removing k digits.
    """
    d = deque(list(num))
    while k > 0 and d:
        while len(d) >= 2 and d[0] == d[1]:
            d.popleft()
            d.popleft()
        d.popleft()
        k -= 1
    res = ''.join(d)
    if len(res) < len(num):
        res += num[0]
    return str(int(res)) if res else '0'