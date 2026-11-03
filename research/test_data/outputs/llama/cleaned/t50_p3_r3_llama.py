from collections import Counter

def find_all_anagrams(s: str, p: str) -> list:
    """
    Find all start indices of anagrams of substring p in string s.

    Args:
        s (str): The main string.
        p (str): The pattern to look for anagrams of.

    Returns:
        list: A list of start indices where an anagram of p starts.
    """
    if len(p) > len(s):
        return []
    p_counter = Counter(p)
    s_window = {}
    start_indices = []
    for i in range(len(s)):
        char = s[i]
        s_window[char] = s_window.get(char, 0) + 1
        if i >= len(p):
            prev_char = s[i - len(p)]
            s_window[prev_char] -= 1
            if s_window[prev_char] == 0:
                del s_window[prev_char]
        if Counter(s_window) == p_counter:
            start_indices.append(i - len(p) + 1)
    return start_indices