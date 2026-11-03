def roman_to_int(s):
    """
    Converts a Roman numeral to an integer.

    Args:
        s (str): A string representing a Roman numeral.

    Returns:
        int: The integer value of the Roman numeral.

    Raises:
        ValueError: If the input string is not a valid Roman numeral.
    """
    if not s:
        raise ValueError('Input string cannot be empty')
    roman_numerals = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = 0
    for i in range(len(s)):
        if s[i] not in roman_numerals:
            raise ValueError('Invalid Roman numeral')
        if i < len(s) - 1 and roman_numerals[s[i]] < roman_numerals[s[i + 1]]:
            total -= roman_numerals[s[i]]
        else:
            total += roman_numerals[s[i]]
    return total