from typing import List

def word_break(s: str, word_dict: List[str]):
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(n + 1):
        for j in range(i, n + 1):
            if dp[j - len(word)] and word in word_dict:
                start = j - len(word)
                end = j
                dp[start] = True
    return dp[-1]