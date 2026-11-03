def roman_to_int(s):
    """
    Converts a Roman numeral to an integer.

    Args:
        s (str): The Roman numeral to be converted.

    Returns:
        int: The integer value of the Roman numeral.

    Raises:
        ValueError: If the input is not a valid Roman numeral.
    """
    if not s:
        raise ValueError('Input cannot be an empty string.')
    roman_values = {'M': 1000, 'D': 500, 'C': 100, 'L': 50, 'X': 10, 'V': 5, 'I': 1}
    total = 0
    prev_value = 0
    for i in range(len(s)):
        if s[i] not in roman_values:
            raise ValueError('Invalid Roman numeral.')
        curr_value = roman_values[s[i]]
        if prev_value < curr_value and i != len(s) - 1:
            raise ValueError('Invalid Roman numeral: Subtractitive notation not allowed.')
        total += curr_value
        prev_value = curr_value
    return total