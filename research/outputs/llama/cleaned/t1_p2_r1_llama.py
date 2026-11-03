def roman_to_int(s: str) -> int:
    """
    Converts Roman numerals to integers.
    
    Parameters:
    s (str): The Roman numeral string.
    
    Returns:
    int: The integer value of the Roman numerals.

    Raises:
    ValueError: If the input contains invalid characters or formatting.
    """
    roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    result = 0
    if not s:
        raise ValueError('Input must be a non-empty string.')
    for i, char in enumerate(s):
        try:
            num = roman_map[char.upper()]
            if i > 0 and num > roman_map[s[i - 1].upper()]:
                raise ValueError('Invalid subtractive notation.')
            result += num
        except KeyError:
            raise ValueError(f"Invalid input: '{char}' is not a valid Roman numeral.")
    return result