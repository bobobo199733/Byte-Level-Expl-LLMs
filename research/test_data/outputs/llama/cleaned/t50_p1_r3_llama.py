from collections import Counter

def find_all_anagrams(s, p):
    """
    Find all start indices in string s where an anagram of string p begins.
    
    Args:
        s (str): The string to search for anagrams.
        p (str): The string to find anagrams of.

    Returns:
        list: A sorted list of starting indices where an anagram of p is found in s.
    """
    result = []
    p_counter = Counter(p)
    left = 0
    for right in range(len(s)):
        while len(s[left:right + 1]) < len(p) or Counter(s[left:right + 1]) != p_counter:
            left += 1
        if right - left + 1 == len(p):
            result.append(left)
    return sorted(result)