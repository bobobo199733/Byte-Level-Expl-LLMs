def basic_calculator(s):

    def update_stack(stack, operator, value):
        if operator == '+':
            stack.append(value)
        elif operator == '-':
            stack.append(-value)

    def evaluate_stack(stack):
        result = 0
        for item in stack:
            result += item
        return result
    s = s.replace(' ', '')
    stack = []
    num = 0
    operator = '+'
    for i, char in enumerate(s + '+'):
        if char.isdigit():
            num = num * 10 + int(char)
        elif char in ['+', '-']:
            update_stack(stack, operator, num)
            operator = char
            num = 0
    return evaluate_stack(stack)