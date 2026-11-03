def remove_k_digits(num: str, k: int) -> str:
    if len(num) <= k:
        return '0' if not num else num
    stack = []
    for digit in num:
        while stack and stack[-1] > digit and (k > 0):
            stack.pop()
            k -= 1
        stack.append(digit)
    result = stack[:len(num) - k]
    return ''.join(result).zfill(len(result) or 1) if result else '0'