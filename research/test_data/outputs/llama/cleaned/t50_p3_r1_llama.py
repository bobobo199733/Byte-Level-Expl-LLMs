from collections import Counter

def find_all_anagrams(s, p):
    """
    Return a list of all start indices in s where an anagram of p starts.

    Args:
        s (str): The string to search for anagrams.
        p (str): The pattern string.

    Returns:
        list: A list of start indices where an anagram of p is found.
    """
    if len(p) > len(s):
        return []
    p_counter = Counter(p)
    result = []
    left, right = (0, 0)
    while right < len(s):
        if s[right] in p_counter:
            p_counter[s[right]] += 1
        while p_counter <= Counter(s[left:right + 1]):
            result.append(left)
            p_counter[s[left]] -= 1
            if p_counter[s[left]] == 0:
                del p_counter[s[left]]
            left += 1
        right += 1
    return result