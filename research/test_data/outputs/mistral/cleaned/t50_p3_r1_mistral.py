def find_all_anagrams(s, p):
    result = []
    window = {}
    need = {}
    for char in p:
        if char not in need:
            need[char] = 0
        need[char] += 1
    start = 0
    end = 0
    while end < len(s):
        char = s[end]
        if char in window:
            window[char] += 1
        else:
            window[char] = 1
        if len(window) == len(need):
            for char, count in need.items():
                if char not in window or window[char] < count:
                    break
            else:
                result.append(start)
        if end + 1 < len(s):
            end += 1
        else:
            break
        if s[start] in need and window[s[start]] == need[s[start]]:
            del need[s[start]]
        start += 1
    return result