def roman_to_int(s: str) -> int:
    roman_values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    for char in s:
        if char not in roman_values:
            raise ValueError('Invalid Roman numeral: contains invalid characters')
    result = 0
    prev_value = 0
    for char in reversed(s):
        curr_value = roman_values[char]
        if curr_value < prev_value:
            result -= curr_value
        else:
            result += curr_value
        prev_value = curr_value
    return result