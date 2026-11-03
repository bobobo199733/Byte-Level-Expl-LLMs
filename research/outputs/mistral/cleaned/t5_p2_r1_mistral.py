from typing import List

def remove_k_digits(num: str, k: int) -> str:
    stack = []
    for digit in num:
        while stack and len(stack) > k - 1 and (stack[-1] > digit):
            stack.pop()
        stack.append(digit)
    stack = [num[0]] + list(filter(lambda x: x != '0', stack))
    if not stack:
        return '0'
    return ''.join(stack)