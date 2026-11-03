def roman_to_int(s: str) -> int:
    """
    Converts a Roman numeral string into its integer value.
    
    Args:
        s (str): A string representing a Roman numeral, using standard symbols I, V, X, L, C, D, M.
        
    Returns:
        int: The integer equivalent of the input Roman numeral string.
        
    Raises:
        ValueError: If the input contains invalid characters or if subtractive notation is used incorrectly.
    """
    roman_numerals = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    result = 0
    prev_value = 0
    for numeral in s:
        if numeral not in roman_numerals:
            raise ValueError(f'Invalid Roman numeral: {numeral}')
        current_value = roman_numerals[numeral]
        if current_value >= prev_value:
            result += current_value
        else:
            raise ValueError(f'Invalid subtractive notation: {numeral}')
        prev_value = current_value
    return result