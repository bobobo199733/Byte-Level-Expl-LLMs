def remove_k_digits(num: str, k: int) -> str:
    if len(num) <= k:
        return '0' if not num else num
    stack = []
    for digit in num:
        while stack and stack[-1] > digit and (k > 0):
            stack.pop()
            k -= 1
        stack.append(digit)
    remaining_digits = stack[:-k]
    result = ''.join(sorted(remaining_digits))
    return result or '0'