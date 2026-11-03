precedence = {'^': 3, '*', '/': 2, '+', '-': 1}
operators = {op: i for i, op in enumerate(["^", "*", "/", "+", "-"])}

def expression_to_postfix(expression):
    def apply_operator(s1, s2, operator):
        if operator == '+':
            return str(float(s1) + float(s2))
        elif operator == '-':
            return str(float(s1) - float(s2))
        elif operator == '*':
            return str(float(s1) * float(s2))
        elif operator == '/':
            return str(float(s1) / float(s2))

    def greater_precedence(op1, op2):
        return precedence[op2] > precedence[op1]

    stack = []
    output = []

    for token in expression:
        if token.isdigit():
            output.append(token)
        elif token in operators:
            while (stack and not stack[-1] == '(') and greater_precedence(operators[token], operators[stack[-1]]):
                output.append(stack.pop())
            stack.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()

    while stack:
        output.append(stack.pop())

    return "".join(output)