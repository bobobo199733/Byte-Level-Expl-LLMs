def is_balanced(s: str) -> bool:
    stack = []
    for c in s:
        if c in '({[':
            stack.append(c)
        elif c in ')}]':
            try:
                last_opening_bracket = stack.pop()
                opening_brackets_map = {'(': ')', '[': ']', '{': '}'}
                if opening_brackets_map[last_opening_bracket] != c:
                    return False
            except IndexError:
                return False
    return len(stack) == 0