def word_break(s, word_dict):
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(1, n + 1):
        for j in range(i, n + 1):
            if dp[j - len(word)] and s[j - len(word):j] == word:
                dp[i] = True
                break
        for word in word_dict:
            if i + len(word) > n:
                continue
            if dp[i + len(word)]:
                dp[i] = True
                break
    return dp[-1]