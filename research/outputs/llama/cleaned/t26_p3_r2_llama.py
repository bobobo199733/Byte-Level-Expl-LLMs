from collections import defaultdict

def min_window_substring(s, t):
    """
    Returns the shortest substring of s that contains all characters of t.

    Args:
        s (str): The string to search in.
        t (str): The string containing the characters to search for.

    Returns:
        str: The shortest substring of s that contains all characters of t. If no such substring exists, returns an empty string.
    """
    if not s or not t:
        return ''
    t_freq = defaultdict(int)
    for char in t:
        t_freq[char] += 1
    min_window_len = float('inf')
    min_window = ''
    formed_chars = 0
    left = 0
    window_freq = defaultdict(int)
    for right, char in enumerate(s):
        window_freq[char] += 1
        if char in t_freq and window_freq[char] <= t_freq[char]:
            formed_chars += 1
        while left <= right and formed_chars == len(t):
            if right - left + 1 < min_window_len:
                min_window_len = right - left + 1
                min_window = s[left:right + 1]
            char_at_left = s[left]
            window_freq[char_at_left] -= 1
            if char_at_left in t_freq and window_freq[char_at_left] < t_freq[char_at_left]:
                formed_chars -= 1
            left += 1
    return min_window