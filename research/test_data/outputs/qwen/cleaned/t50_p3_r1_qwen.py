from collections import Counter

def find_all_anagrams(s: str, p: str) -> list:
    if len(p) > len(s):
        return []
    pattern_count = Counter(p)
    window_count = Counter(s[:len(p)])
    result = [0] if window_count == pattern_count else []
    for i in range(len(s) - len(p)):
        window_count[s[i]] -= 1
        window_count[s[i + len(p)]] += 1
        if window_count == pattern_count:
            result.append(i + 1)
    return result