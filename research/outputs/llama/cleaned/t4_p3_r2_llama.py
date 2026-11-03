def decode_string(s: str) -> str:
    stack = []
    cur_num = ''
    cur_str = ''
    for c in s:
        if c.isdigit():
            cur_num += c
        elif c == '[':
            stack.append(cur_str)
            stack.append(int(cur_num))
            cur_str = ''
            cur_num = ''
        elif c == ']':
            num = stack.pop()
            prev_str = stack.pop()
            cur_str = prev_str + num * cur_str
        else:
            cur_str += c
    if stack:
        raise ValueError('Invalid input')
    return cur_str