def remove_k_digits(num, k):
    stack = []
    for digit in num:
        while stack and stack[-1] > digit and k:
            stack.pop()
            k -= 1
        stack.append(digit)
    stack = stack[:-k]
    result = ''.join(stack)
    if not result:
        return '0'
    return ''.join(filter(bool, result))