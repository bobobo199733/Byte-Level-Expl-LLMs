def decode_string(s: str) -> str:

    def recursive_decode(s, cur_num):
        stack = []
        i = 0
        while i < len(s):
            if s[i].isdigit():
                j = i
                while j < len(s) and s[j].isdigit():
                    j += 1
                cur_num = int(s[i:j])
                i = j
            elif s[i] == '[':
                stack.append((cur_num, i))
                i += 1
            else:
                if not stack:
                    return ''
                num, start = stack.pop()
                end = i - 1
                result = recursive_decode(s[start + 1:end], cur_num) * num
                i = end + 1
        result = ''.join((recursive_decode('' + s[i], 0) for i in range(0, len(s), 2)))
        if not stack and result:
            return result
        else:
            raise ValueError('Invalid input')
    return recursive_decode(s, 0)