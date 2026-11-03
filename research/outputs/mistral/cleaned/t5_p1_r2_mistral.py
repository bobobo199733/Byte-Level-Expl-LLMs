def remove_k_digits(num: str, k: int) -> str:

    def helper(stack, num):
        if not num:
            return ''.join(stack) or '0'
        top = stack[-1] if stack else None
        while num and top and (int(top) > int(num[0])):
            stack.pop()
            k -= 1
            if not k:
                break
            if not num:
                return ''.join(stack)
            helper(stack, num[1:])
        if num:
            helper(stack + [num[0]], num[1:])
    helper([], list(num))