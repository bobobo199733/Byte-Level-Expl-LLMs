def find_all_anagrams(s, p):
    result = []
    table = {}
    for char in p:
        if char not in table:
            table[char] = 0
        table[char] += 1
    window_start = 0
    window = {}
    match_length = len(p)
    for end in range(len(s)):
        right_char = s[end]
        if right_char not in window:
            window[right_char] = 0
        window[right_char] += 1
        while match_length <= len(s):
            if table == dict(window):
                result.append(window_start)
            if window_start < end and s[window_start] == s[end]:
                window_count = window[s[window_start]] - 1
                if window_count == 0:
                    del window[s[window_start]]
                else:
                    window[s[window_start]] = window_count
            window_start += 1
        match_length += 1
    return sorted(result)