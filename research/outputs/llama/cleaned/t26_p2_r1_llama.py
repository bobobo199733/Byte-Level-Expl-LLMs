def min_window_substring(s, t):
    """
    Find the minimum window in s containing every character from t.

    Args:
        s (str): The input string.
        t (str): The target string.

    Returns:
        str: The minimum window substring or an empty string if no valid window exists.
    """
    if not t or len(t) > len(s):
        return ''
    s_count = {}
    t_count = {}
    required_chars = 0
    formed_chars = 0
    left = 0
    for char in t:
        if char not in t_count or t_count[char] == 0:
            required_chars += 1
        t_count[char] = t_count.get(char, 0) + 1
    min_window = (float('inf'), None, None)
    for right in range(len(s)):
        if s[right] in t_count:
            s_count[s[right]] = s_count.get(s[right], 0) + 1
            if s_count[s[right]] <= t_count[s[right]]:
                formed_chars += 1
        while formed_chars == required_chars and left <= right:
            if right - left + 1 < min_window[0]:
                min_window = (right - left + 1, left, right)
            if s[left] in t_count:
                if s_count[s[left]] == t_count[s[left]]:
                    formed_chars -= 1
                s_count[s[left]] -= 1
            left += 1
    return '' if min_window[0] == float('inf') else s[min_window[1]:min_window[2] + 1]