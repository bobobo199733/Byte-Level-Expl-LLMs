def min_window_substring(s, t):
    from collections import Counter
    need = Counter(t)
    missing = len(t)
    start, start_index = (0, -1)
    left = 0
    for right in range(len(s)):
        if s[right] in need:
            if need[s[right]] > 0:
                missing -= 1
            need[s[right]] -= 1
        while missing == 0:
            if start_index == -1 or right - left < start_index - start:
                start_index = right - left + 1
                start = left
            if s[left] in need:
                need[s[left]] += 1
                if need[s[left]] > 0:
                    missing += 1
            left += 1
    return s[start:start_index] if start_index != -1 else ''