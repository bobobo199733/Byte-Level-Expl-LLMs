from collections import defaultdict

def min_window_substring(s, t):
    result = None
    window = defaultdict(int)
    need = defaultdict(int)
    min_length = float('inf')
    for char in t:
        need[char] += 1
    start = end = len(t)
    for i, char in enumerate(s):
        window[char] += 1
        while start <= i:
            if all((window[key] >= need[key] for key in need)):
                while end < len(s) and all((window[key] >= need[key] for key in need)):
                    end += 1
                    window[s[end - 1]] -= 1
                temp_length = end - start
                if temp_length < min_length:
                    min_length = temp_length
                    result = s[start:end]
                start += 1
                window[s[start - 1]] -= 1
    return result