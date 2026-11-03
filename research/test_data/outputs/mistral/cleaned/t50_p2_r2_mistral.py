from collections import Counter

def find_all_anagrams(s, p):
    if len(p) > len(s):
        return []
    anagrams = []
    window = Counter()
    result = Counter(p)
    start = 0
    for end in range(len(s)):
        window[s[end]] += 1
        if end >= len(p) - 1:
            if result == window:
                anagrams.append(start)
            window[s[start]] -= 1
            if window[s[start]] == 0:
                del window[s[start]]
            start += 1
    return sorted(anagrams)