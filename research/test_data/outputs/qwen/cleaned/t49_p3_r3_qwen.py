def word_break(s, word_dict):
    dp = [False] * (len(s) + 1)
    dp[0] = True
    for i in range(1, len(s) + 1):
        for word in word_dict:
            if len(word) <= i and s[:i].endswith(word):
                if dp[i - len(word)]:
                    dp[i] = True
                    break
    return dp[len(s)]