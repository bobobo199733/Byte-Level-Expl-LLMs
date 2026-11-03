def roman_to_int(s):
    valid_symbols = {'I', 'V', 'X', 'L', 'C', 'D', 'M'}
    numerals = {'IV': 4, 'IX': 9, 'XL': 40, 'XC': 90, 'CD': 400, 'CM': 900}
    max_repeat = 3
    if not s:
        raise ValueError('Empty string is not allowed.')
    for symbol in s:
        if symbol not in valid_symbols:
            raise ValueError(f'Invalid Roman numeral symbol: {symbol}')
        if symbol in {'I', 'X', 'C', 'M'} and s.count(symbol) > max_repeat:
            raise ValueError(f"Too many consecutive repetitions of '{symbol}'.")
        if symbol in ('V', 'L', 'D') and s.count(symbol) > 1:
            raise ValueError(f"Repeated occurrence of '{symbol}' is not allowed.")
        for pair in numerals:
            if symbol + pair[0] in s and pair[1] + symbol in s:
                raise ValueError(f'Invalid Roman numeral combination: {symbol}{pair[0]} and {pair[1]}{symbol}')
    roman_value = sum([s.count(symbol) for symbol in valid_symbols])
    for pair in numerals:
        roman_value -= numerals[pair] * (s.count(pair[0]) if pair[0] not in s[1:] else s.count(pair[1]) - 1)
    return roman_value