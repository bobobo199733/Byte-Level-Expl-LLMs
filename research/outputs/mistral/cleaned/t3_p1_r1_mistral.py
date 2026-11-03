def evaluate(expr):

    def _evaluate(tokens, precedence=None):
        operators = {'+': 1, '-': 1, '*': 2, '/': 2}
        stack = []
        for token in tokens:
            if token.isdigit():
                stack.append(int(token))
            elif token in operators:
                op2 = stack.pop()
                op1 = stack.pop()
                if not precedence or operators[token] <= precedence:
                    if token in {'+', '-'}:
                        stack.append(op1 + op2)
                    else:
                        stack.append(op1 // op2)
            elif token == '(':
                stack_copy = [token] + list(_evaluate(tokens[tokens.index(token) + 1:]))
                _evaluate(stack_copy, precedence)
            elif token == ')':
                while stack and stack[-1] != '(':
                    stack.pop()
                stack.pop()
        return stack[0]
    tokens = list(filter(lambda x: x and x not in [' ', '\t'], expr))
    return _evaluate(tokens)