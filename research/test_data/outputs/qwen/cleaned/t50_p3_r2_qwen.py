from collections import Counter

def find_all_anagrams(s: str, p: str) -> list:
    if len(p) > len(s):
        return []
    target_counter = Counter(p)
    window_counter = Counter()
    result = []
    left = 0
    for right in range(len(s)):
        window_counter[s[right]] += 1
        if right - left + 1 == len(p):
            if window_counter == target_counter:
                result.append(left)
            window_counter[s[left]] -= 1
            if window_counter[s[left]] == 0:
                del window_counter[s[left]]
            left += 1
    return result