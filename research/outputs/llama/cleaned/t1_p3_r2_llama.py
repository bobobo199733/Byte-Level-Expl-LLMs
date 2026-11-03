def roman_to_int(s: str) -> int:
    if not s:
        raise ValueError('Input cannot be empty')
    mapping = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    subtractive_pairs = {'IV', 'IX', 'XL', 'XC', 'CD', 'CM'}
    i = 0
    result = 0
    while i < len(s):
        if s[i] not in mapping:
            raise ValueError(f"Invalid symbol '{s[i]}' at position {i + 1}")
        value = mapping[s[i]]
        if i + 1 < len(s) and s[i:i + 2] in subtractive_pairs:
            result += value - 5 * mapping[s[i + 1]]
            i += 2
        else:
            result += value
            i += 1
            if s[i - 1] == 'I' and s[i - 3:i] == 'III':
                raise ValueError('Repeated I at position {} is invalid'.format(i))
            elif s[i - 1] == 'X' and s[i - 3:i] == 'XXX':
                raise ValueError('Repeated X at position {} is invalid'.format(i))
            elif s[i - 1] == 'C' and s[i - 3:i] == 'CCC':
                raise ValueError('Repeated C at position {} is invalid'.format(i))
            elif s[i - 1] == 'M' and s[i - 3:i] == 'MMM':
                raise ValueError('Repeated M at position {} is invalid'.format(i))
            if i < len(s) and s[i] in ['V', 'L', 'D'] and (s[i] == s[i - 1]):
                raise ValueError(f'Repeated {s[i]} at position {i + 1} is invalid')
    return result