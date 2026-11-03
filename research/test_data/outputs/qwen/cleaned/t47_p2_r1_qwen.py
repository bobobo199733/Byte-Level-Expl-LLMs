def basic_calculator(s):

    def compute(stack, operator, operand):
        if operator == '+':
            return stack.pop() + operand
        elif operator == '-':
            return stack.pop() - operand
    s = s.replace(' ', '')
    result_stack = []
    current_number = 0
    current_operator = '+'
    for i, char in enumerate(s):
        if char.isdigit():
            current_number = current_number * 10 + int(char)
        if not char.isdigit() or i == len(s) - 1:
            if current_operator == '+':
                result_stack.append(current_number)
            elif current_operator == '-':
                result_stack.append(-current_number)
            current_operator = char
            current_number = 0
    return sum(result_stack)