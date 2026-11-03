def roman_to_int(s):
    roman_dict = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    if not s:
        raise ValueError('The input string cannot be empty.')
    total = 0
    for i in range(len(s)):
        current_value = roman_dict[s[i]]
        if i + 1 < len(s):
            next_value = roman_dict[s[i + 1]]
            if current_value > next_value:
                raise ValueError(f"Invalid Roman numeral '{s}'. Only standard subtractive notation is allowed.")
            elif current_value < next_value:
                total += next_value - current_value
                i += 1
        else:
            total += current_value
    return total