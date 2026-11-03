def edit_distance(word1: str, word2: str) -> int:
    """
    Returns the minimum number of edits needed to transform one string into another.
    
    Args:
        word1 (str): The original word.
        word2 (str): The target word.
    
    Returns:
        int: The minimum edit distance between the two words.
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