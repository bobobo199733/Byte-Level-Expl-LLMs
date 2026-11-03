def word_break(s, word_dict):
    dp = [False] + [False] * len(s)
    words = set(word_dict)
    for i in range(1, len(s) + 1):
        for j in range(i):
            if dp[j] and s[j:i] in words:
                dp[i] = True
    return dp[-1]