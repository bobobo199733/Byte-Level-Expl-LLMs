def basic_calculator(s):

    def compute_expression(tokens):
        stack = []
        current_number = 0
        operation = '+'
        for token in tokens:
            if token.isdigit():
                current_number = current_number * 10 + int(token)
            elif token == '(':
                i, j = (stack.pop(), len(stack) - 1)
                inner_result = compute_expression(stack[i + 1:j])
                stack[j - 1] = str(inner_result)
            else:
                if operation == '+':
                    stack.append(current_number)
                elif operation == '-':
                    stack.append(-current_number)
                current_number = 0
                operation = token
        if operation == '+':
            stack.append(current_number)
        elif operation == '-':
            stack.append(-current_number)
        return sum(stack)
    s = s.replace(' ', '')
    tokens = []
    i = 0
    while i < len(s):
        if s[i].isdigit():
            j = i + 1
            while j < len(s) and s[j].isdigit():
                j += 1
            tokens.append(int(s[i:j]))
            i = j - 1
        elif s[i] == '(':
            count = 1
            j = i + 1
            while j < len(s):
                if s[j] == '(':
                    count += 1
                elif s[j] == ')':
                    count -= 1
                if count == 0:
                    break
                j += 1
            tokens.append(compute_expression(s[i + 1:j].split()))
        i += 1
    return compute_expression(tokens)