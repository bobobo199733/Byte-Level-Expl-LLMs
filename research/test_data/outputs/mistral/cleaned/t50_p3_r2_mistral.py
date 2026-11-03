def find_all_anagrams(s, p):
    result = []
    window = Collections.defaultdict(int)
    char_frequency = Collections.Counter(p)
    for end in range(len(s)):
        window[s[end]] += 1
        while len(window) > len(char_frequency):
            window[s[end - len(window)]] -= 1
            if window[s[end - len(window)]] == 0:
                del window[s[end - len(window)]]
        if window == char_frequency and end >= len(p) - 1:
            result.append(end - len(p) + 1)
    return result