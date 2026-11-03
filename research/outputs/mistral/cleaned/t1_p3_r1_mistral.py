def roman_to_int(s):
    if not s:
        raise ValueError('Empty string is not allowed')
    valid = {'I', 'V', 'X', 'L', 'C', 'D', 'M'}
    if not all((c in valid for c in s)):
        raise ValueError('Input contains invalid characters')
    symbols_count = {c: s.count(c) for c in valid}
    for symbol in ['IV', 'IX', 'XL', 'XC', 'CD', 'CM']:
        if symbol in s and symbols_count[symbol[0]] >= 3 or symbols_count[symbol[1]] >= 3:
            raise ValueError('Invalid numeral structure')
    total = 0
    for i in range(len(s) - 1, -1, -1):
        current = s[i]
        if current in ['I', 'X', 'C'] and (i < len(s) - 1 and s[i + 1] not in [current[:-1], 'V', 'L', 'D']) or current in ['V', 'L', 'D']:
            next_symbol = s[i + 1] if i < len(s) - 1 else None
            if current in ['X', 'C'] and next_symbol == current[:-1]:
                total += sum([5 * symbols_count[current], 10 * symbols_count[next_symbol]])
            elif current in ['I', 'V', 'L'] and next_symbol in [current[:-1], 'D']:
                total += sum([4 * symbols_count[current], 5 * symbols_count[next_symbol]])
            else:
                total += symbols_count[current]
        else:
            total += symbols_count[current]
    return total