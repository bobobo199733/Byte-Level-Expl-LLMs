def basic_calculator(s):

    def apply_operator(operand1, operand2, operator):
        if operator == '+':
            return operand1 + operand2
        elif operator == '-':
            return operand1 - operand2

    def handle_parentheses(expression):
        stack = []
        current_number = 0
        for char in expression:
            if char.isdigit():
                current_number = current_number * 10 + int(char)
            elif char == '(':
                stack.append((current_number, None))
                current_number = 0
            elif char == ')':
                prev_operand, operator = stack.pop()
                result = apply_operator(prev_operand, current_number, operator)
                if stack:
                    last_operand = stack[-1][0]
                    stack[-1] = (last_operand + result, None)
                else:
                    return result
            elif char in ('+', '-'):
                if current_number != 0:
                    prev_operand, operator = stack[-1]
                    stack[-1] = (apply_operator(prev_operand[0], current_number, operator), None)
                    current_number = 0
                else:
                    stack.append((None, char))
        if current_number != 0:
            stack[-1] = (stack[-1][0] + current_number, None)
        return stack[0][0]
    return handle_parentheses(s)