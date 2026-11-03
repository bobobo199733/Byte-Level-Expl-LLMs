def operaters_precedence(op):
    if op == '+' or op == '-':
        return 1
    elif op == '*' or op == '/':
        return 2

def basic_calculator(s):

    def apply_operation(operand1, operand2, op):
        if op == '+':
            return operand1 + operand2
        else:
            return operand1 - operand2
    stack = []
    operator_stack = []
    numbers = re.findall('-\\d+|\\d+', s)
    for token in numbers + list(s):
        if token.isdigit():
            stack.append(int(token))
        elif token == '(':
            operator_stack.append(token)
        elif token == ')':
            while operator_stack[-1] != '(':
                pop_operator = operator_stack.pop()
                second_operand = stack.pop()
                first_operand = stack.pop()
                result = apply_operation(first_operand, second_operand, pop_operator)
                stack.append(result)
            operator_stack.pop()
        elif token in ['+', '-', '*', '/']:
            while len(operator_stack) > 0 and operaters_precedence(token) <= operaters_precedence(operator_stack[-1]):
                pop_operator = operator_stack.pop()
                second_operand = stack.pop()
                first_operand = stack.pop()
                result = apply_operation(first_operand, second_operand, pop_operator)
                stack.append(result)
            operator_stack.append(token)
    while len(operator_stack) > 0:
        pop_operator = operator_stack.pop()
        second_operand = stack.pop()
        first_operand = stack.pop()
        result = apply_operation(first_operand, second_operand, pop_operator)
        stack.append(result)
    return stack[0]