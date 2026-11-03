def is_balanced(s):

    def check_brackets(stack, bracket):
        if not stack:
            return False
        while stack and stack[-1] != bracket:
            stack.pop()
        if stack and stack[-1] == bracket:
            stack.pop()
        return not stack
    brackets = {')': '(', ']': '[', '}': '{'}
    open_brackets = []
    for char in s:
        if char in brackets:
            if not open_brackets or open_brackets[-1] != brackets[char]:
                return False
            open_brackets.pop()
        elif char not in brackets and char not in '(), [], {}':
            continue
        open_brackets.append(char)
    return not open_brackets