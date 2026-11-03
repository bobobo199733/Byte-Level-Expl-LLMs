def roman_to_int(s):
    roman_values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    if not s:
        raise ValueError('Input cannot be an empty string.')
    prev_value = -1
    total = 0
    for char in s:
        if char not in roman_values:
            raise ValueError(f'Invalid Roman numeral: {char}')
        current_value = roman_values[char]
        if prev_value < current_value:
            total += current_value - 2 * prev_value
        else:
            total += current_value
        prev_value = current_value
    return total