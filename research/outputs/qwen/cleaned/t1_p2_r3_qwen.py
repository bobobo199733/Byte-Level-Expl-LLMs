def roman_to_int(s: str) -> int:
    roman_values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    if not s:
        raise ValueError('Input cannot be an empty string')
    total = 0
    prev_value = 0
    for char in reversed(s):
        value = roman_values.get(char)
        if value is None:
            raise ValueError(f'Invalid character: {char}')
        if value < prev_value:
            total -= value
        else:
            total += value
        prev_value = value
    return total