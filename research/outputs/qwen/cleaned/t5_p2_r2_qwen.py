def remove_k_digits(num: str, k: int) -> str:
    if not num or k >= len(num):
        return '0'
    stack = []
    for digit in num:
        while k > 0 and stack and (stack[-1] > digit):
            stack.pop()
            k -= 1
        stack.append(digit)
    final_num = ''.join(stack[:-k if k else None])
    return str(int(final_num))