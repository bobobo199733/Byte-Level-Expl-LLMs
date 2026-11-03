def json_validator(text):
    brackets = {'{': '}', '[': ']', '"': '"', "'": "'"}
    stack = []
    i = 0
    while i < len(text):
        char = text[i]
        if char in "{'[":
            if not stack or (len(stack) > 0 and brackets[stack[-1]] != char):
                return False
            stack.append(brackets[char])
        elif char == '}':
            if len(stack) == 0 or stack.pop() != '{':
                return False
        elif char == ']':
            if len(stack) == 0 or stack.pop() != '[':
                return False
        elif char in ",'":
            pass
        elif not (char.isspace() or char.isdigit() or char.isalpha() or (char in '\'"')):
            return False
        i += 1
    return len(stack) == 0