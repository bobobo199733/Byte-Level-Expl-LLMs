def min_window_substring(s, t):
    """
    Find the minimum window in s containing every character from t.

    Args:
        s (str): The string to search in.
        t (str): The target characters to find.

    Returns:
        str: The minimum window in s containing every character from t. If no valid window exists, returns an empty string.
    """
    if not t or len(t) > len(s):
        return ''
    t_count = {}
    for char in t:
        if char not in t_count:
            t_count[char] = 1
        else:
            t_count[char] += 1
    min_window = ''
    min_len = float('inf')
    left = 0
    formed = 0
    window_counts = {}
    for right in range(len(s)):
        char = s[right]
        if char not in window_counts:
            window_counts[char] = 1
        else:
            window_counts[char] += 1
        if char in t_count and window_counts[char] == t_count[char]:
            formed += 1
        while left <= right and formed == len(t):
            if right - left + 1 < min_len:
                min_len = right - left + 1
                min_window = s[left:right + 1]
            char = s[left]
            window_counts[char] -= 1
            if char in t_count and window_counts[char] < t_count[char]:
                formed -= 1
            left += 1
    return min_window