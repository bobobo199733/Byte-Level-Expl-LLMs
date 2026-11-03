from collections import Counter

def find_all_anagrams(s: str, p: str) -> list[int]:
    """
    Find all anagram starting indices in string s of length p.

    Args:
        s (str): The input string.
        p (str): The pattern string for which to find anagrams.

    Returns:
        list[int]: A sorted list of starting indices where the pattern is an anagram of the corresponding substring in s.
    """
    if len(p) > len(s):
        return []
    p_freq = Counter(p)
    window_freq = {}
    start_indices = []
    window_size = len(p)
    for i in range(len(s)):
        if i < window_size:
            window_freq[s[i]] = window_freq.get(s[i], 0) + 1
        if i >= window_size - 1 and Counter(window_freq) == p_freq:
            start_indices.append(i - window_size + 1)
        if i > 0 and i >= window_size - 1:
            removed_char = s[i - window_size]
            window_freq[removed_char] -= 1
            if window_freq[removed_char] == 0:
                del window_freq[removed_char]
    return sorted(start_indices)