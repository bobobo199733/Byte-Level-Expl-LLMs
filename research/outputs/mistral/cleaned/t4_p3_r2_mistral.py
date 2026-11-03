import re

def decode_string(s):

    def _decode(match):
        count, inner = match.group(1, 2)
        return count * _decode(inner) if inner else count
    pattern = re.compile('(\\d+)\\[([^\\]\\\\]+)\\]')
    result = pattern.sub(_decode, s)
    try:
        return result
    except Exception as e:
        raise ValueError('Invalid input') from e