def roman_to_int(s):
    """
    Converts a Roman numeral to an integer.

    Parameters:
    s (str): A string representing a Roman numeral.

    Returns:
    int: The integer value of the Roman numeral.

    Raises:
    ValueError: If the input is not a valid Roman numeral.
    """
    if not s or len(s) == 0:
        raise ValueError('Input cannot be empty')
    roman_numerals = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    result = 0
    i = 0
    while i < len(s):
        if i + 1 < len(s) and s[i] in ['I', 'X', 'C'] and (s[i + 1] in ['V', 'L', 'D']):
            if (s[i:i + 2] == 'IV' or s[i:i + 2] == 'IX') and i + 2 < len(s):
                result += roman_numerals[s[i + 2]]
                i += 3
            elif (s[i:i + 2] == 'XL' or s[i:i + 2] == 'XC') and i + 2 < len(s):
                result += roman_numerals[s[i + 2]]
                i += 3
            elif (s[i:i + 2] == 'CD' or s[i:i + 2] == 'CM') and i + 2 < len(s):
                result += roman_numerals[s[i + 2]]
                i += 3
            else:
                raise ValueError('Invalid Roman numeral')
        else:
            if s[i] not in roman_numerals:
                raise ValueError('Invalid character in input')
            if roman_numerals[s[i]] != 0:
                result += roman_numerals[s[i]]
            i += 1
    return result