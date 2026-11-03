def word_break(s, word_dict):
    if not s:
        return True
    dp = [False] * (len(s) + 1)
    dp[0] = True
    for i in range(len(s)):
        for j in range(i + 1, len(s) + 1):
            if dp[j - 1] and s[j - 1:] in word_dict:
                dp[j] = True
                break
    return dp[-1]