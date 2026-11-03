def remove_k_digits(num, k):
    stack = []
    for digit in num:
        while stack and stack[-1] > digit and (k > 0):
            stack.pop()
            k -= 1
        stack.append(digit)
    while stack and stack[-1] == '0':
        stack.pop()
    if not stack:
        return '0' if k else ''
    return ''.join(stack)