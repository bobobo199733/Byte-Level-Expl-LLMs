def min_window_substring(s, t):
    from collections import Counter
    t_count = Counter(t)
    required = len(t_count)
    left, right = (0, 0)
    formed = 0
    window_counts = {}
    ans = (float('inf'), None, None)
    while right < len(s):
        character = s[right]
        window_counts[character] = window_counts.get(character, 0) + 1
        if character in t_count and window_counts[character] == t_count[character]:
            formed += 1
        while left <= right and formed == required:
            character = s[left]
            if right - left + 1 < ans[0]:
                ans = (right - left + 1, left, right)
            window_counts[character] -= 1
            if character in t_count and window_counts[character] < t_count[character]:
                formed -= 1
            left += 1
        right += 1
    return '' if ans[0] == float('inf') else s[ans[1]:ans[2] + 1]