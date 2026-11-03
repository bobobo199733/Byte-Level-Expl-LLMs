def find_all_anagrams(s: str, p: str) -> list:
    from collections import Counter
    if len(p) > len(s):
        return []
    counter_p = Counter(p)
    counter_window = Counter()
    result_indices = []
    left, right = (0, len(p) - 1)
    while right < len(s):
        counter_window[s[right]] += 1
        if left > 0:
            counter_window[s[left - 1]] -= 1
            if counter_window[s[left - 1]] == 0:
                del counter_window[s[left - 1]]
        if counter_p == counter_window:
            result_indices.append(left)
        left += 1
        right += 1
    return sorted(result_indices)