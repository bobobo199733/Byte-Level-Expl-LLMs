def roman_to_int(s):
    valid = {'I', 'V', 'X', 'L', 'C', 'D', 'M'}
    subtractive = {('IV', 4), ('IX', 9), ('XL', 40), ('XC', 90), ('CD', 400), ('CM', 900)}
    if not s:
        raise ValueError('Empty string')
    for char in s:
        if char not in valid:
            raise ValueError(f"Invalid character '{char}'")
    result = 0
    i = len(s) - 1
    while i >= 0:
        char, num = (None, 0)
        for c, n in subtractive:
            if s[i:i + len(c)] == c:
                char, num = (c[0], num)
                break
        if not char:
            char = s[i]
            if char in ('I', 'X', 'C'):
                if s[i - 3:i + 1].count(char) > 3:
                    raise ValueError(f"Repetition error for '{char}'")
            elif char in ('V', 'L', 'D'):
                if s[i - 1] == char:
                    raise ValueError(f"Repeat error for '{char}'")
        num = int(num)
        result += num * valid.index(char)
        i -= len(char)
    return result