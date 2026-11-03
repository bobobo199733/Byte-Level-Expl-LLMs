def decode_string(s):

    def _decode_string(acc, seq):
        if not seq:
            return acc
        number, pattern = (seq[0], seq[1:])
        multiplier = int(number)
        result = acc * multiplier
        if number == '0':
            return result
        if pattern[0] != '[':
            raise ValueError('Invalid input')
        for char in _decode_string('', pattern):
            result += char * multiplier
        return result
    if not s:
        return ''
    if not s[0].isdigit() or (len(s) > 1 and (not s[1] == '[')):
        raise ValueError('Invalid input')
    return _decode_string('', [s])