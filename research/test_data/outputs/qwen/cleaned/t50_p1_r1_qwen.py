def find_all_anagrams(s, p):
    from collections import Counter
    len_s = len(s)
    len_p = len(p)
    target_count = Counter(p)
    window_count = Counter()
    result = []
    for i in range(len_s):
        window_count[s[i]] += 1
        if i >= len_p:
            char_to_remove = s[i - len_p]
            window_count[char_to_remove] -= 1
            if window_count[char_to_remove] == 0:
                del window_count[char_to_remove]
        if i >= len_p - 1 and window_count == target_count:
            result.append(i - len_p + 1)
    return sorted(result)