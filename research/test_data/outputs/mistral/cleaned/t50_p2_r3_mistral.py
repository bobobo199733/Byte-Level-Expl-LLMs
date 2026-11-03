from collections import Counter

def find_all_anagrams(s, p):
    if not p or len(p) > len(s):
        return []
    result = []
    counter_p = Counter(p)
    counter_window = Counter()
    left = right = 0
    while right < len(s):
        counter_window[s[right]] += 1
        if right - left + 1 >= len(p):
            if counter_window == counter_p:
                result.append(left)
            counter_window[s[left]] -= 1
            if counter_window[s[left]] == 0:
                del counter_window[s[left]]
            left += 1
        right += 1
    return sorted(result)