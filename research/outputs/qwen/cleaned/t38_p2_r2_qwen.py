def expression_to_postfix(expression):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    stack = []
    output = []
    expression = expression.replace(' ', '')
    for char in expression:
        if char.isalnum():
            output.append(char)
        elif char == '(':
            stack.append(char)
        elif char == ')':
            top_element = stack.pop()
            while top_element != '(':
                output.append(top_element)
                top_element = stack.pop()
        else:
            while stack and stack[-1] in precedence and (precedence[stack[-1]] >= precedence[char]):
                output.append(stack.pop())
            stack.append(char)
    while stack:
        output.append(stack.pop())
    return ''.join(output)