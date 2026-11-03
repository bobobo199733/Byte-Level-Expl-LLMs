def expression_to_postfix(expression):
    operators = ['+', '-', '*', '/', '^']
    valid_operators = ['+', '-', '*', '/', '^', '(', ')']

    def is_operator(c):
        return c in operators

    def has_higher_precedence(op1, op2):
        return precedence[op1] > precedence[op2]

    def apply_operators(stack):
        i = 0
        while not stack:
            if i >= len(expression) or (not is_operator(expression[i]) and expression[i] != '('):
                stack.append(expression[i])
                i += 1
            elif is_operator(expression[i]) and expression[i] != '(' or (expression[i] == '(' and (not stack)):
                while not stack or (stack[-1] != '(' and has_higher_precedence(stack[-1], expression[i])):
                    stack.pop()
                stack.append(expression[i])
                i += 1
            elif expression[i] == ')':
                while stack[-1] != '(':
                    stack.pop()
                stack.pop()
                i += 1
            else:
                while not stack or (stack[-1] != '(' and has_higher_precedence(stack[-1], expression[i])):
                    result = stack.pop()
                    postfix.append(result)
                stack.append(expression[i])
                i += 1
        while stack:
            postfix.append(stack.pop())
    postfix = []
    for c in expression:
        if is_operator(c) or c == '(':
            apply_operators(stack)
        elif c == ')':
            apply_operators(stack)
        else:
            postfix.append(c)
    return ' '.join(postfix)