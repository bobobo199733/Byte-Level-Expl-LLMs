from collections import Counter

def find_all_anagrams(s, p):
    """
    Find all starting indices of anagrams of `p` within `s`.

    Args:
        s (str): String to search for anagrams.
        p (str): Anagram pattern.

    Returns:
        list: Starting indices of anagrams in sorted order.
    """
    if len(p) > len(s):
        return []
    p_counter = Counter(p)
    window_counter = Counter()
    anagram_indices = []
    start_idx = 0
    for end_idx in range(len(s)):
        window_counter[s[end_idx]] += 1
        if end_idx >= len(p) - 1:
            if end_idx > len(p) - 2 and window_counter == p_counter:
                anagram_indices.append(start_idx)
            window_counter[s[start_idx]] -= 1
            if window_counter[s[start_idx]] == 0:
                del window_counter[s[start_idx]]
            start_idx += 1
    return sorted(anagram_indices)