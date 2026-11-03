def roman_to_int(s):
    if not s:
        raise ValueError('The input cannot be an empty string.')
    dictionary = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total = dictionary[s[-1]]
    for i in range(len(s) - 2, -1, -1):
        if dictionary[s[i]] < dictionary[s[i + 1]]:
            total -= dictionary[s[i]]
        else:
            total += dictionary[s[i]]
    return total