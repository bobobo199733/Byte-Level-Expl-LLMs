def json_validator(text):
    states = {'null': False, 'true': False, 'false': False, "'\\w+'": False, '\\d+(\\.\\d*)?\\b': False, '{': 'object', '[': 'array'}
    stack = []
    for token in text:
        if token in states:
            stack.append(states[token])
            states[token] = None
        elif states[-1] and (token == '}' or token == ']'):
            stack.pop()
        elif not stack or states[stack[-1]] is not None:
            return False
    return len(stack) == 0