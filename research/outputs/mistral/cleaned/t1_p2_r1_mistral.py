def roman_to_int(s: str) -> int:
    if not all((char in ROMAN_VALUES for char in s)):
        raise ValueError('Invalid Roman numeral')
    num = 0
    for i in range(len(s)):
        if i > 0 and ROMAN_VALUES[s[i - 1]] > ROMAN_VALUES[s[i]]:
            raise ValueError('Incorrect subtractive notation')
        num += ROMAN_VALUES[s[i]]
    return num