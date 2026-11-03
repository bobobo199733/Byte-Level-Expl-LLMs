from collections import Counter

def find_all_anagrams(s, p):
    if len(p) > len(s):
        return []
    p_count = Counter(p)
    window_count = Counter()
    result_indices = []
    left = 0
    for right in range(len(s)):
        window_count[s[right]] += 1
        while right - left + 1 > len(p):
            window_count[s[left]] -= 1
            if window_count[s[left]] == 0:
                del window_count[s[left]]
            left += 1
        if right - left + 1 == len(p) and p_count == window_count:
            result_indices.append(left)
    return sorted(result_indices)