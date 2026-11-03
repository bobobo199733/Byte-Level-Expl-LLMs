def evaluate(expr: str) -> int:
    import re

    def tokenize(s):
        return [t for t in re.findall('\\d+|[-+*/()]', s)]
    tokens = tokenize(expr.replace(' ', ''))
    stack, num, sign = ([], 0, '+')
    ops = {'+': lambda x: x, '-': lambda x: -x, '*': lambda x: x * num, '/': lambda x: int(x / num)}
    for i, token in enumerate(tokens + ['']):
        if token.isdigit():
            num = int(token)
        elif token in '+-*/':
            if sign == '+':
                stack.append(num)
            elif sign == '-':
                stack.append(-num)
            elif sign == '*':
                stack.append(stack.pop() * num)
            elif sign == '/':
                stack.append(int(stack.pop() / num))
            sign = token
            num = 0
        elif token == '(':
            j = 1
            for k in range(i + 1, len(tokens)):
                if tokens[k] == ')':
                    j -= 1
                elif tokens[k] == '(':
                    j += 1
                if not j:
                    return stack.append(evaluate(''.join(tokens[i + 1:k]))) or evaluate(''.join(tokens[k + 1:])) + sum(stack)
        if i == len(tokens) - 1 and sign in ops:
            if sign == '+':
                stack.append(num)
            elif sign == '-':
                stack.append(-num)
            elif sign == '*':
                stack.append(stack.pop() * num)
            else:
                stack.append(int(stack.pop() / num))
    return sum(stack)