def word_break(s, word_dict):
    dp = {len(s) + 1: False}
    dp[0] = True
    for i in range(1, len(s) + 1):
        for word in word_dict:
            if i - len(word) >= 0 and s[i - len(word):i] == word:
                if i not in dp or not dp[i]:
                    dp[i] = True
                    for j in range(i + len(word), len(s) + 1):
                        if j in dp and dp[j]:
                            dp[i] = True
                            break
    return dp[len(s)]