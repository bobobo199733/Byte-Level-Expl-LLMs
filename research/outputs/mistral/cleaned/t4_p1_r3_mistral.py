def decode_string(s):

    def helper(seq, accumulator):
        if not seq:
            return accumulator
        number, pattern = (seq[0], seq[1:])
        multiplier = int(number)
        result = accumulator * multiply_pattern(pattern)
        return helper(pattern, result) if pattern else result

    def multiply_pattern(pattern):
        if not pattern:
            return ''
        number, remaining = (pattern[0], pattern[1:])
        multiplier = int(number)
        return multiplier * result if number.isdigit() else result + multiply_pattern(remaining)
    try:
        return helper(s[1:-1].split(), '')
    except ValueError as e:
        raise ValueError('Invalid input: ' + str(e))