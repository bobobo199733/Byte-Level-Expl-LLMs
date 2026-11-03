import re

def decode_string(s):

    def helper(match):
        count, sequence = match.group(1, 2)
        result = ''
        for char in helper(sequence) * int(count):
            result += char
        return result
    pattern = '(\\d+)\\[([^[]*|\\\\[])*\\]'
    if not s or re.match(pattern, s) is None:
        raise ValueError('Invalid input')
    return helper(re.search(pattern, s))