from collections import defaultdict

def min_window_substring(s: str, t: str) -> str:
    """
    This function finds the smallest window in string `s` that contains all characters of string `t`.
    
    Args:
        s (str): The string to search for the window.
        t (str): The string containing the characters to search for.

    Returns:
        str: The shortest part of `s` containing all characters of `t`, or an empty string if no such window exists.
    """
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
        if char in t_freq:
            window_counts[char] += 1
            if window_counts[char] == t_freq[char]:
                formed += 1
        while left <= right and formed == len(t_freq):
            if right - left + 1 < min_len:
                min_len = right - left + 1
                min_window = s[left:right + 1]
            char = s[left]
            if char in t_freq:
                window_counts[char] -= 1
                if window_counts[char] < t_freq[char]:
                    formed -= 1
            left += 1
    return min_window