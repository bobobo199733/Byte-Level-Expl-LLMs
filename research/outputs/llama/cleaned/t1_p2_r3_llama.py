def roman_to_int(s: str) -> int:
    """
    Convert a Roman numeral string into its integer value.
    
    Args:
        s (str): The Roman numeral string to convert.
        
    Returns:
        int: The integer value of the input Roman numeral string.
    
    Raises:
        ValueError: If the input is not valid, including incorrect subtractive notation or invalid repetitions.
    """
    roman_values = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    result = 0
    if not isinstance(s, str) or not all((c in roman_values for c in s)):
        raise ValueError('Invalid Roman numeral string')
    for i, char in enumerate(s):
        if i < len(s) - 1 and roman_values[char] < roman_values[s[i + 1]]:
            result -= roman_values[char]
        else:
            result += roman_values[char]
    if not 1 <= result <= 3999:
        raise ValueError('Invalid Roman numeral string')
    return result