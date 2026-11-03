def min_window_substring(s, t):
    need = {}
    window = {}
    min_length = float('inf')
    result = ''
    for char in t:
        need[char] = need.get(char, 0) + 1
    start = end = len(t) - 1
    while end < len(s):
        char = s[end]
        end_need = need.get(char, 0)
        if end_need > 0:
            window[char] = window.get(char, 0) + 1
            while start < end and window[s[start]] > need.get(s[start], 0):
                window[s[start]] -= 1
                start += 1
            if start == end:
                start += 1
            if all((w >= n for w, n in window.items() if n > 0)) and end - start + 1 < min_length:
                min_length = end - start + 1
                result = s[start:end + 1]
        end += 1
    return result