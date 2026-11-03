from collections import Counter

def find_all_anagrams(s, p):
    if len(p) > len(s):
        return []
    p_counter = Counter(p)
    s_counter = Counter()
    result_indices = []
    left, right = (0, len(p) - 1)
    while right < len(s):
        s_counter[s[right]] += 1
        if right >= len(p):
            s_counter[s[left]] -= 1
            left += 1
        if p_counter == s_counter:
            result_indices.append(left)
        right += 1
    return result_indices