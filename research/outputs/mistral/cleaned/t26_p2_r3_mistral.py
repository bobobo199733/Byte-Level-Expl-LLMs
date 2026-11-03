def min_window_substring(s, t):
    need = {}
    wind = {}
    left, right, minlen, count = (0, 0, len(s) + 1, len(t))
    for c in t:
        need[c] = need.get(c, 0) + 1
    while right < minlen:
        ch = s[right]
        wind[ch] = wind.get(ch, 0) + 1
        if ch in need and wind[ch] >= need[ch]:
            count -= 1
        right += 1
        while left < right and count == 0:
            ch = s[left]
            wind[ch] -= 1
            if ch in need and wind[ch] < need[ch]:
                count += 1
            left += 1
        if minlen > right - left:
            minlen = right - left
    return s[left:minlen + left] if minlen != len(s) + 1 else ''