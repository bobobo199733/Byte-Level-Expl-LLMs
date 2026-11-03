def remove_k_digits(num: str, k: int) -> str:
    stack = []
    for digit in num:
        while stack and k > 0 and (stack[-1] > digit):
            k -= 1
            stack.pop()
        stack.append(digit)
    while k > 0:
        stack.pop()
        k -= 1
    return ''.join(stack).lstrip('0') or '0'