def wildcard_match(s: str, p: str) -> bool:
    """
    Return True if the entire string s matches the wildcard pattern p, otherwise return False.

    Rules:
    - '?' matches exactly one character
    - '*' matches any sequence of characters, including the empty sequence
    - Matching must cover the entire string
    """
    if len(p) == 0 and len(s) > 0:
        return False
    if len(p) == 0 and len(s) != 0:
        return False
    dp = [[False] * (len(p) + 1) for _ in range(len(s) + 1)]
    dp[0][0] = True
    for j in range(1, len(p) + 1):
        if p[j - 1] == '*':
            dp[0][j] = dp[0][j - 1]
    for i in range(1, len(s) + 1):
        for j in range(1, len(p) + 1):
            if p[j - 1] == '*':
                dp[i][j] = dp[i][j - 1] or dp[i - 1][j]
            elif p[j - 1] == '?':
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = dp[i - 1][j - 1] and s[i - 1] == p[j - 1]
    return dp[len(s)][len(p)]