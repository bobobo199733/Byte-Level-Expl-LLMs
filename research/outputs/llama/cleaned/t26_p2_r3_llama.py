def min_window_substring(s: str, t: str) -> str:
    """
    Finds the minimum window in s containing every character from t.

    Args:
        s (str): The string to search within.
        t (str): The characters required to be present in the window.

    Returns:
        str: The minimum window substring. If no valid window exists, an empty string is returned.
    """
    t_count = {}
    for char in t:
        if char in t_count:
            t_count[char] += 1
        else:
            t_count[char] = 1
    required_chars = len(t_count)
    formed_chars = 0
    window_counts = {}
    left = 0
    min_length = float('inf')
    min_window = ''
    for right in range(len(s)):
        char = s[right]
        if char in t_count:
            window_counts[char] = window_counts.get(char, 0) + 1
            if window_counts[char] == t_count[char]:
                formed_chars += 1
        while left <= right and formed_chars == required_chars:
            char = s[left]
            if right - left + 1 < min_length:
                min_length = right - left + 1
                min_window = s[left:right + 1]
            if char in t_count:
                window_counts[char] -= 1
                if window_counts[char] < t_count[char]:
                    formed_chars -= 1
            left += 1
    return min_window