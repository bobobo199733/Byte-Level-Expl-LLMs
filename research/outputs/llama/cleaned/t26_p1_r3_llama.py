from collections import defaultdict

def min_window_substring(s: str, t: str) -> str:
    """
    Returns the smallest substring of `s` containing all characters from `t`.
    
    Args:
        s (str): The string to search for a substring in.
        t (str): The string whose characters should be contained within the result.
    
    Returns:
        str: The smallest substring of `s` that contains all characters from `t`. If no such substring exists, an empty string is returned.
    """
    if not s or not t:
        return ''
    t_counts = defaultdict(int)
    for c in t:
        t_counts[c] += 1
    required_chars = len(t_counts)
    formed_chars = 0
    window_counts = defaultdict(int)
    left, right = (0, 0)
    min_window_size = float('inf')
    min_window_start = 0
    while right < len(s):
        character = s[right]
        window_counts[character] += 1
        if character in t_counts and window_counts[character] == t_counts[character]:
            formed_chars += 1
        while formed_chars == required_chars:
            if right - left + 1 < min_window_size:
                min_window_size = right - left + 1
                min_window_start = left
            character = s[left]
            window_counts[character] -= 1
            if character in t_counts and window_counts[character] < t_counts[character]:
                formed_chars -= 1
            left += 1
        right += 1
    return '' if min_window_size == float('inf') else s[min_window_start:min_window_start + min_window_size]