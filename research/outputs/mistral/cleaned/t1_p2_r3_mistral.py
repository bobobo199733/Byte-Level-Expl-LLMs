def roman_to_int(s):
    roman_values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    result = 0
    prev_numerals = ''
    for i in range(len(s)):
        current_numerals = s[i]
        if i > 0 and roman_values[current_numerals] > roman_values[prev_numerals]:
            raise ValueError('Invalid Roman numeral: subtractive notation is not allowed')
        prev_numerals = current_numerals
        result += roman_values.get(current_numerals, 0)
    return result