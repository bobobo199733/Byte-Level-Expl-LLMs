def roman_to_int(s):
    if not s:
        raise ValueError('The input string cannot be empty')
    roman_dict = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    result = 0
    prev_value = 0
    for char in s[::-1]:
        current_value = roman_dict.get(char)
        if not current_value:
            raise ValueError(f"Invalid Roman numeral '{char}'")
        if prev_value > current_value:
            raise ValueError(f'Invalid Roman numeral (subtractive notation violation): {s}')
        result += current_value
        prev_value = current_value
    return result