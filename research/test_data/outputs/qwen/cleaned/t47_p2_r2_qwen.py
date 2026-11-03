def basic_calculator(s):

    def calculate(stack, sign=1):
        res = 0
        num = 0
        while stack:
            item = stack.pop()
            if isinstance(item, int):
                num = item * sign + num
            elif item == '+':
                res += num
                num = 0
            elif item == '-':
                res += num
                num = 0
                sign *= -1
            elif item == '(':
                stack.append(res)
                stack.append(sign)
                break
        if num != 0:
            res += num * sign
        return res
    s = s.replace(' ', '')
    stack = []
    current_number = None
    current_sign = 1
    i = 0
    while i < len(s):
        if s[i].isdigit():
            start = i
            while i + 1 < len(s) and s[i + 1].isdigit():
                i += 1
            current_number = int(s[start:i + 1])
            stack.append(current_number)
        elif s[i] in '+-':
            if current_number is not None:
                stack.append(current_number)
                current_number = None
            stack.append(s[i])
            current_sign = 1 if s[i] == '+' else -1
        elif s[i] == '(':
            stack.append(current_number or 0)
            stack.append(current_sign)
            current_number = None
            current_sign = 1
            i += 1
            while s[i] != ')':
                if s[i].isdigit():
                    start = i
                    while i + 1 < len(s) and s[i + 1].isdigit():
                        i += 1
                    stack.append(int(s[start:i + 1]))
                    current_number = None
                elif s[i] in '+-':
                    if current_number is not None:
                        stack.append(current_number)
                        current_number = None
                    stack.append(s[i])
                    current_sign = 1 if s[i] == '+' else -1
                i += 1
            stack.pop()
            stack.append(calculate(stack, current_sign))
        i += 1
    if current_number is not None:
        stack.append(current_number)
    return calculate(stack)