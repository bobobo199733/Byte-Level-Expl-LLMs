def roman_to_int(s: str) -> int:
    if s == '':
        raise ValueError
    numeral_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    prev_value = 0
    total = 0
    for char in s:
        if char not in numeral_map:
            raise ValueError
        value = numeral_map[char]
        if prev_value and (char == 'V' or char == 'X') and (prev_value * 5 != value):
            raise ValueError
        elif prev_value and (char == 'L' or char == 'C') and (prev_value * 50 != value):
            raise ValueError
        elif prev_value and (char == 'D' or char == 'M') and (prev_value * 500 != value):
            raise ValueError
        if prev_value and value > prev_value:
            total += value - 2 * prev_value
        else:
            total += value
        prev_value = value
    for i in range(len(s) - 1):
        if s[i] == 'I' and s[i + 1] not in ['V', 'X'] or (s[i] == 'X' and s[i + 1] not in ['L', 'C']) or (s[i] == 'C' and s[i + 1] not in ['D', 'M']):
            raise ValueError
    if prev_value * 4 > total:
        raise ValueError
    return total