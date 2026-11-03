def edit_distance(word1: str, word2: str) -> int:
    """
    Compute the Levenshtein distance between two strings.

    This function uses dynamic programming to efficiently compute the minimum number of operations (insertions, deletions, substitutions)
    required to transform one string into another.

    Args:
        word1 (str): The first string.
        word2 (str): The second string.

    Returns:
        int: The Levenshtein distance between the two strings.
    """
    m, n = (len(word1), len(word2))
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if word1[i - 1] == word2[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost)
    return dp[m][n]