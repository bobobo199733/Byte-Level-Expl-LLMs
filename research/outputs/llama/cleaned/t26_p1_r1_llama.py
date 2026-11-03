from collections import defaultdict

def min_window_substring(s: str, t: str) -> str:
    """
    Returns the smallest substring of `s` containing all characters from `t`.

    Args:
        s (str): The string to search for a substring in.
        t (str): The string containing the characters to search for.

    Returns:
        str: The smallest substring of `s` containing all characters from `t`.
             If no such substring exists, returns an empty string.
    """
    if len(t) > len(s) or (not t and (not s)):
        return ''
    t_freq = defaultdict(int)
    for char in t:
        t_freq[char] += 1
    min_window = ''
    min_len = float('inf')
    left = 0
    formed = 0
    window_counts = defaultdict(int)
    for right in range(len(s)):
        char = s[right]
        window_counts[char] += 1
        if char in t_freq and window_counts[char] == t_freq[char]:
            formed += 1
        while left <= right and formed == len(t_freq):
            char = s[left]
            if right - left + 1 < min_len:
                min_len = right - left + 1
                min_window = s[left:right + 1]
            window_counts[char] -= 1
            if char in t_freq and window_counts[char] < t_freq[char]:
                formed -= 1
            left += 1
    return min_window