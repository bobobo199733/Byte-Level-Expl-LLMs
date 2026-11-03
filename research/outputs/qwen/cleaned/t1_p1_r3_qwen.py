def roman_to_int(s):
    roman_values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    if not s:
        raise ValueError('Input string cannot be empty')
    total = 0
    prev_value = 0
    for char in reversed(s):
        value = roman_values.get(char, None)
        if value is not None and prev_value > 0 and (value < prev_value):
            raise ValueError('Invalid Roman numeral')
        if value is not None and value < prev_value:
            total -= value
        else:
            total += value
        prev_value = value
    return total