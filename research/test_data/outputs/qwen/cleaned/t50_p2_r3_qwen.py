from collections import Counter

def find_all_anagrams(s, p):
    if len(p) > len(s):
        return []
    p_count = Counter(p)
    s_count = Counter()
    left = 0
    anagram_indices = []
    for right in range(len(s)):
        s_count[s[right]] += 1
        if right - left + 1 > len(p):
            s_count[s[left]] -= 1
            if s_count[s[left]] == 0:
                del s_count[s[left]]
            left += 1
        if p_count == s_count:
            anagram_indices.append(left)
    return anagram_indices