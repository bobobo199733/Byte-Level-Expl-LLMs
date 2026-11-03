def edit_distance(word1, word2):
    """
    Compute the Levenshtein distance between two strings.
    
    This function supports insertions, deletions, and substitutions.
    
    Parameters:
    word1 (str): The first string.
    word2 (str): The second string.
    
    Returns:
    int: The Levenshtein distance between word1 and word2.
    """
    m = len(word1) + 1
    n = len(word2) + 1
    dp = [[0] * n for _ in range(m)]
    for i in range(1, m):
        dp[i][0] = i
    for j in range(1, n):
        dp[0][j] = j
    for i in range(1, m):
        for j in range(1, n):
            cost = 0 if word1[i - 1] == word2[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost)
    return dp[m - 1][n - 1]