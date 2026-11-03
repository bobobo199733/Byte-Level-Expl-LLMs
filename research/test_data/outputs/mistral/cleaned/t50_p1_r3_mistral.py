from collections import Counter

def find_all_anagrams(s, p):
    result = []
    counter_p = Counter(p)
    window_counter = Counter()
    for i in range(len(s)):
        if i >= len(p):
            window_counter[s[i - len(p)]] -= 1
            if window_counter[s[i - len(p)]] < 0:
                window_counter.pop(s[i - len(p)])
        while i >= 0 and len(window_counter) == len(counter_p):
            if counter_p == window_counter:
                result.append(i - len(p))
            if i > 0:
                window_counter[s[i - 1]] -= 1
                if window_counter[s[i - 1]] < 0:
                    window_counter.pop(s[i - 1])
            i -= 1
        if i < len(s) - 1:
            window_counter[s[i + 1]] += 1
    return sorted(result)