def decode_string(s):

    def decode_helper(stack, seq):
        if not seq:
            return ''.join(stack)
        count, seq = (seq[0], seq[1:])
        multiplier = '' if count == '[]' else count
        if multiplier:
            stack.append(decode_helper(stack, seq * int(multiplier)))
        elif seq[0] == '[' and seq[-1] == ']':
            result = decode_helper(stack, seq[1:-1])
            stack.append(result)
        else:
            stack.append(seq)
        return decode_helper(stack, seq)
    return decode_helper([], s) if s else ''