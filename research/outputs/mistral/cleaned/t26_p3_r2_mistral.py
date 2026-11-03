def min_window_substring(s, t):
    if not t:
        return ""

    result = (None, None)  # To store the result: (start index, length)
    window = {}
    needs = {}

    for char in t:
        needs[char] = needs.get(char, 0) + 1

    start = end = -1
    min_len = len(s) + 1

    for i, char in enumerate(s):
        if char in needs:
            window[char] = window.get(char, 0) + 1
            if char in needs and window[char] == needs[char]:
                while start < i:
                    if s[start] in window:
                        window[s[start]] -= 1
                        if window[s[start]] < needs[s[start]]:
                            break
                    start += 1
                if not result[0]:
                    result = (start, i - start + 1)
                    min_len = result[1]
                else:
                    new_len = result[1] - (i - start)
                    if new_len < min_len:
                        min_len = new_len
                        result = (start, new_len)

    return result[0]:None if not result else s[result[0]:result[0]+result[1]]