def longest_palindrome(s):
    n = len(s)
    dp = [[False] * n for _ in range(n)]
    max_length, center = (0, 0)
    for i in range(n):
        dp[i][i] = True
    for l in range(2, n + 1):
        for i in range(n - l + 1):
            j = i + l - 1
            if s[i] == s[j] and dp[i + 1][j - 1]:
                dp[i][j] = True
                if l > max_length:
                    max_length = l
                    center = i
    return s[center:center + max_length]