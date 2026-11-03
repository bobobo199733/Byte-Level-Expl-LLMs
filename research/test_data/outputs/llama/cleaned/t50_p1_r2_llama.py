from collections import Counter

def find_all_anagrams(s: str, p: str) -> list:
    """
    Finds all start indices in string s where an anagram of string p begins.
    
    Args:
        s (str): The input string to search for anagrams.
        p (str): The string whose anagrams we're looking for.

    Returns:
        list: A sorted list of starting indices where an anagram of p begins.
    """
    if len(p) > len(s):
        return []
    p_count = Counter(p)
    left = 0
    right = 0
    match_count = len(p)
    indices = []
    while right < len(s):
        if s[right] in p_count:
            p_count[s[right]] -= 1
            if p_count[s[right]] == 0:
                match_count += 1
        if right - left + 1 == len(p) and match_count == len(p):
            indices.append(left)
        if right - left + 1 == len(p):
            if s[left] in p_count:
                p_count[s[left]] += 1
                if p_count[s[left]] > 0:
                    match_count -= 1
            left += 1
        right += 1
    return sorted(indices)