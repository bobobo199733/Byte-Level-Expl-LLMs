def remove_k_digits(num: str, k: int) -> str:
    stack = []
    for digit in num:
        while k and stack and (stack[-1] > digit):
            stack.pop()
            k -= 1
        stack.append(digit)
    result = ''.join(stack[:-k if k else 0])
    return str(int(result.lstrip('0'))) if result.lstrip('0') else '0'