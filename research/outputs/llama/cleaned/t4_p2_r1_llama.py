def decode_string(s: str) -> str:
    stack = []
    curr_num = ''
    curr_str = ''
    for ch in s:
        if ch.isdigit():
            curr_num += ch
        elif ch == '[':
            stack.append(curr_str)
            stack.append(int(curr_num or 1))
            curr_str, curr_num = ('', '')
        elif ch == ']':
            num = stack.pop()
            prev_str = stack.pop()
            curr_str = prev_str + num * curr_str
        else:
            curr_str += ch
    return curr_str