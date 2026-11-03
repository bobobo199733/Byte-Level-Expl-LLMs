from collections import Counter

def find_all_anagrams(s, p):
    if not p or len(p) > len(s):
        return []
    counter_p = Counter(p)
    counter_window = Counter()
    anagrams = []
    start = 0
    for end in range(len(s)):
        counter_window[s[end]] += 1
        if counter_window[s[end]] <= counter_p[s[end]]:
            pass
        elif counter_window[s[end]] > counter_p[s[end]]:
            while start < end:
                counter_window[s[start]] -= 1
                if counter_window[s[start]] == counter_p[s[start]] or counter_window[s[start]] < counter_p[s[start]]:
                    break
                start += 1
        if counter_window == counter_p:
            anagrams.append(start)
    return sorted(anagrams)