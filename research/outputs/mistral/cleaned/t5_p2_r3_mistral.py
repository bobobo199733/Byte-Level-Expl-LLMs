def remove_k_digits(num: str, k: int) -> str:
    if not num or k == 0:
        return ''
    stack = []
    for digit in num:
        while stack and stack[-1] > digit and (k > 0):
            stack.pop()
            k -= 1
        stack.append(digit)
    while stack and k > 0:
        stack.pop()
        k -= 1
    result = num[:len(stack)]
    for digit in num[len(stack):]:
        if not result or int(digit) < int(result[-1]):
            result += digit
    while result and result[0] == '0':
        result = result[1:]
    return result