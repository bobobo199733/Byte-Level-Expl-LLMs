def min_window_substring(s, t):
    window = {}
    need = {}
    minlen = float('inf')
    start = 0
    for char in t:
        if char not in need:
            need[char] = 0
        need[char] += 1
    for end in range(len(s)):
        right = s[end]
        if right in need:
            window[right] = window.get(right, 0) + 1
            if right in need and window[right] == need[right]:
                while True:
                    to_remove = start
                    start += 1
                    if s[to_remove] in window:
                        if window[s[to_removed]] > 0:
                            window[s[to_removed]] -= 1
                        else:
                            break
                    if start - to_remove < minlen:
                        minlen = start - to_remove
                    if len(window) == len(need):
                        break
    return s[start:minlen + start] if minlen != float('inf') else ''