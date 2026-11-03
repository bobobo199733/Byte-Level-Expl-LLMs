def wildcard_match(s: str, p: str) -> bool:
    """
    Checks whether a string matches a wildcard pattern.

    Args:
        s (str): The input string.
        p (str): The wildcard pattern where '?' matches one character and '*' matches any sequence of characters.

    Returns:
        bool: True if the string matches the pattern, False otherwise.
    """
    dp = [[False] * (len(p) + 1) for _ in range(len(s) + 1)]
    dp[0][0] = True
    for j in range(1, len(p) + 1):
        if p[j - 1] == '*':
            dp[0][j] = dp[0][j - 1]
    for i in range(1, len(s) + 1):
        for j in range(1, len(p) + 1):
            if s[i - 1] == p[j - 1] or p[j - 1] == '?':
                dp[i][j] = dp[i - 1][j - 1]
            elif p[j - 1] == '*':
                dp[i][j] = dp[i - 1][j] or dp[i][j - 1]
    return dp[len(s)][len(p)]