from collections import Counter

def find_all_anagrams(s: str, p: str) -> list[int]:
    """
    Returns a list of all starting indices in s where the substring 
    matches the anagram of p.
    
    Parameters:
    s (str): The string to search for anagrams.
    p (str): The pattern to find anagrams for.
    
    Returns:
    list[int]: A list of all starting indices where the substring is an anagram of p, sorted in ascending order.
    """
    if len(p) > len(s):
        return []
    p_counter = Counter(p)
    left = 0
    right = len(p)
    result = []
    s_counter = Counter(s[:len(p)])
    while right <= len(s):
        if s_counter == p_counter:
            result.append(left)
        s_counter[s[left]] -= 1
        if s_counter[s[left]] == 0:
            del s_counter[s[left]]
        left += 1
        if right <= len(s):
            s_counter[s[right - 1]] = s_counter.get(s[right - 1], 0) + 1
            right += 1
    return sorted(result)