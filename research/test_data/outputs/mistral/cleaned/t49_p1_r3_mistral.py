from typing import List

def word_break(s: str, word_dict: List[str]):
    words = set(word_dict)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(1, n + 1):
        for j in range(i, min(i + 30, n + 1)):
            if dp[j - i] and s[j - i:j] in words:
                dp[i] = True
                break
    return dp[-1]