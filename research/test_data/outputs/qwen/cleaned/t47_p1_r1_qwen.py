def basic_calculator(s: str) -> int:

    def evaluate_expression(stack, sign):
        return stack.pop() * sign
    result = 0
    current_number = 0
    operator = '+'
    for char in s + '+':
        if char.isdigit():
            current_number = current_number * 10 + int(char)
        elif char == '+' or char == '-':
            if operator == '+':
                result += current_number
            elif operator == '-':
                result -= current_number
            operator = char
            current_number = 0

    def parse_parentheses(expression):
        stack, num, sign = ([], 0, '+')
        for i in range(len(expression)):
            if expression[i].isdigit():
                num = num * 10 + int(expression[i])
            elif expression[i] == '(':
                close_parenthesis_idx = find_closing_parenthesis(expression, i)
                temp_num = parse_parentheses(expression[i + 1:close_parenthesis_idx])
                num = evaluate_expression(stack, sign) + (temp_num if sign == '+' else -temp_num)
                i = close_parenthesis_idx
        return evaluate_expression(stack, sign) + num

    def find_closing_parenthesis(expression, start):
        open_count = 1
        for i in range(start + 1, len(expression)):
            if expression[i] == '(':
                open_count += 1
            elif expression[i] == ')':
                open_count -= 1
            if open_count == 0:
                return i
    s = ''.join(s.split())
    result += parse_parentheses(s)
    return result