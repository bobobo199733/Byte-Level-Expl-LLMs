def longest_palindrome(s):
    if not s or len(s) == 1:
        return s
    n = len(s)
    dp = [[False] * n for _ in range(n)]
    max_length = 0
    start = 0
    for i in range(n):
        dp[i][i] = True
    for L in range(2, n + 1):
        for i in range(n - L + 1):
            j = i + L - 1
            if s[i] == s[j] and dp[i + 1][j - 1]:
                dp[i][j] = True
                if L > max_length:
                    start, max_length = (i, L)
    return s[start:start + max_length]