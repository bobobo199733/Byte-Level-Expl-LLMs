def remove_k_digits(num: str, k: int) -> str:
    if not num or k == len(num):
        return ''
    stack = []
    for digit in num:
        while stack and stack[-1] > digit and (k > 0):
            stack.pop()
            k -= 1
        stack.append(digit)
    while stack and stack[0] == '0':
        stack.pop(0)
    if k > 0:
        for _ in range(k):
            stack.pop()
    return ''.join(stack)