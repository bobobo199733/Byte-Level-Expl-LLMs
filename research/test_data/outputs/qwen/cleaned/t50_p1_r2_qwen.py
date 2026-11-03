from collections import Counter

def find_all_anagrams(s, p):
    if len(s) < len(p):
        return []
    p_count = Counter(p)
    window_count = Counter()
    for i in range(len(p)):
        window_count[s[i]] += 1
    result = []
    if p_count == window_count:
        result.append(0)
    for i in range(len(p), len(s)):
        window_count[s[i - len(p)]] -= 1
        if window_count[s[i - len(p)]] == 0:
            del window_count[s[i - len(p)]]
        window_count[s[i]] += 1
        if p_count == window_count:
            result.append(i - len(p) + 1)
    return sorted(result)