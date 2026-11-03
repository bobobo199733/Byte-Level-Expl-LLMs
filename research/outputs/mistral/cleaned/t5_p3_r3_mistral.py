def remove_k_digits(num, k):
    stack = []
    for char in num:
        while stack and stack[-1] > char and (k > 0):
            stack.pop()
            k -= 1
        stack.append(char)
    result = stack[:-k]
    result = ''.join(result).lstrip('0')
    return '0' if not result else result