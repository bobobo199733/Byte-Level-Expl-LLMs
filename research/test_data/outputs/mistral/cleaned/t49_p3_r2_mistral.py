from collections import defaultdict
from typing import List

def word_break(s: str, word_dict: List[str]) -> bool:
    words = set(word_dict)
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(1, n + 1):
        for j in range(0, i):
            if dp[j] and s[j:i] in words:
                dp[i] = True
                break
    return dp[-1]