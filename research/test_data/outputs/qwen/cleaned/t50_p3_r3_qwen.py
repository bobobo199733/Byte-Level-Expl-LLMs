def find_all_anagrams(s, p):
    from collections import Counter
    len_s = len(s)
    len_p = len(p)
    if len_p > len_s:
        return []
    p_count = Counter(p)
    window_count = Counter()
    result = []
    for i in range(len_p):
        window_count[s[i]] += 1
    if p_count == window_count:
        result.append(0)
    for i in range(len_s - len_p):
        window_count[s[i]] -= 1
        window_count[s[i + len_p]] += 1
        if p_count == window_count:
            result.append(i + 1)
    return result