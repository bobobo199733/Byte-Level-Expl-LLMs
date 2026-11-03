from collections import defaultdict

def min_window_substring(s: str, t: str) -> str:
    """
    Returns the shortest substring in string s which contains all characters of string t.

    Args:
        s (str): The main string to search for the substring.
        t (str): The string containing the characters that should be present in the substring.

    Returns:
        str: The shortest substring in s containing all characters of t, or an empty string if no such substring exists.
    """
    if len(t) > len(s):
        return ''
    t_count = defaultdict(int)
    for char in t:
        t_count[char] += 1
    min_window = ''
    min_length = float('inf')
    left = 0
    formed = 0
    window_counts = defaultdict(int)
    for right in range(len(s)):
        character = s[right]
        window_counts[character] += 1
        if character in t_count and window_counts[character] == t_count[character]:
            formed += 1
        while left <= right and formed == len(t_count):
            if right - left + 1 < min_length:
                min_length = right - left + 1
                min_window = s[left:right + 1]
            character = s[left]
            window_counts[character] -= 1
            if character in t_count and window_counts[character] < t_count[character]:
                formed -= 1
            left += 1
    return min_window