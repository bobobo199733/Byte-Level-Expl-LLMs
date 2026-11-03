def min_window_substring(s, t):
    need = {}
    have = {}
    window = ''
    minlen = float('inf')
    minwin = ''
    for char in t:
        need[char] = need.get(char, 0) + 1
    start = end = len(t) - 1
    while end < len(s):
        have[s[end]] = have.get(s[end], 0) + 1
        while have and need:
            if have[s[start]] > need.get(s[start], 0):
                have[s[start]] -= 1
                start += 1
            else:
                window = s[start:end + 1]
                newlen = end - start + 1
                if newlen < minlen:
                    minlen = newlen
                    minwin = window
                if not need or have == need:
                    break
            end += 1
        if not need:
            break
    return minwin