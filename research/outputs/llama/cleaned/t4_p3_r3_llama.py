def decode_string(s: str) -> str:
    stack = []
    cur_num = ''
    prev_char = ''
    cur_str = ''
    for c in s:
        if c.isdigit():
            cur_num += c
        elif c == '[':
            if cur_num != '':
                raise ValueError('Missing repeat count before brackets')
            stack.append(cur_str)
            stack.append(prev_char)
            cur_str, prev_char = ('', '')
        elif c == ']':
            if cur_num == '':
                raise ValueError('Mismatched brackets')
            num = int(cur_num)
            cur_str += num * prev_char
            cur_num, prev_char = ('', '')
            cur_str = stack.pop() + cur_str
            prev_char = stack.pop()
        else:
            if cur_num != '':
                cur_str += cur_num * c
                cur_num = ''
            cur_str += c
    if cur_num != '':
        raise ValueError('Mismatched brackets')
    return cur_str