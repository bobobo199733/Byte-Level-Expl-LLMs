def wildcard_match(s: str, p: str) -> bool:
    """
    Returns True if the entire string s matches the wildcard pattern p, otherwise returns False.

    Rules:
    - '?' matches exactly one character
    - '*' matches any sequence of characters, including the empty sequence
    - Matching must cover the entire string

    :param s: The input string to match against the pattern.
    :type s: str
    :param p: The wildcard pattern to match against the string.
    :type p: str
    :return: True if the string matches the pattern, False otherwise.
    """
    if len(s) == 0:
        for i in range(len(p)):
            if p[i] != '*':
                return False
        return True
    dp = [[False] * (len(p) + 1) for _ in range(len(s) + 1)]
    dp[0][0] = True
    for i in range(1, len(p) + 1):
        if p[i - 1] == '*':
            dp[0][i] = dp[0][i - 1]
    for i in range(1, len(s) + 1):
        for j in range(1, len(p) + 1):
            if p[j - 1] == '*':
                dp[i][j] = dp[i - 1][j] or dp[i][j - 1]
            else:
                dp[i][j] = p[j - 1] == s[i - 1] and dp[i - 1][j - 1]
    return dp[len(s)][len(p)]