from collections import Counter

def find_all_anagrams(s, p):
    """
    Finds all start indices in string s where an anagram of string p begins.
    
    Args:
        s (str): The string to search for anagrams.
        p (str): The string to compare with.
    
    Returns:
        list: A sorted list of starting indices.
    """
    if len(p) > len(s):
        return []
    p_counter = Counter(p)
    count = sum((freq for freq in p_counter.values()))
    left, right = (0, 0)
    anagrams = []
    while right < len(s):
        if s[right] in p_counter:
            p_counter[s[right]] -= 1
            count -= 1
        while left <= right and count != 0:
            anagrams.append(left)
            if s[left] in p_counter:
                p_counter[s[left]] += 1
                count += 1
            left += 1
        right += 1
    return sorted(anagrams)