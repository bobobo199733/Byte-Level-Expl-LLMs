def word_break(s, word_dict):
    dp = [False] * (len(s) + 1)
    dp[0] = True
    word_set = set(word_dict)
    for i in range(1, len(s) + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break
    return dp[-1]