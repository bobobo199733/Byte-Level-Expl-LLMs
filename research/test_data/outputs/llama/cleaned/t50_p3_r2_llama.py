from collections import Counter

def find_all_anagrams(s, p):
    """
    Returns a list of start indices where an anagram of p starts in s.
    
    Args:
        s (str): The string to search for anagrams.
        p (str): The pattern string whose anagrams we're searching for.

    Returns:
        list: List of start indices where an anagram of p is found in s.
    """
    if len(p) > len(s):
        return []
    p_counter = Counter(p)
    required_chars = len(set(p))
    window_counts = Counter()
    start_idx, max_len = (0, len(p))
    anagram_indices = []
    for end_idx, char in enumerate(s):
        if char not in p_counter:
            continue
        window_counts[char] += 1
        while len(window_counts) > required_chars:
            char_at_start = s[start_idx]
            if char_at_start not in p_counter:
                start_idx += 1
                continue
            window_counts[char_at_start] -= 1
            if window_counts[char_at_start] == 0:
                del window_counts[char_at_start]
            start_idx += 1
        if end_idx - start_idx + 1 >= max_len:
            if window_counts == p_counter:
                anagram_indices.append(start_idx)
    return anagram_indices