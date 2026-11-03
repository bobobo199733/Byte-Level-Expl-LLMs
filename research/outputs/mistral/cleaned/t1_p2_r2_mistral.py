def roman_to_int(s: str) -> int:
    if not s or len(set(s)) != len(ROMAN_VALUES):
        raise ValueError('Invalid Roman numeral')
    result = 0
    for i in range(len(s)):
        if i > 0 and ROMAN_VALUES[s[i]] > ROMAN_VALUES[s[i - 1]] or i == len(s) - 1:
            result += ROMAN_VALUES[s[i]]
        elif i < len(s) - 1 and ROMAN_VALUES[s[i]] < ROMAN_VALUES[s[i + 1]]:
            result += ROMAN_VALUES[s[i]]
        else:
            raise ValueError('Incorrect subtractive notation or invalid repetitions')
    return result