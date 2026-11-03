def word_break(s: str, word_dict: list[str]) -> bool:
    """
    Determine if s can be segmented into words from word_dict.

    Args:
    - s (str): Input string.
    - word_dict (list[str]): List of valid words.

    Returns:
    - bool: Whether s can be segmented using words from word_dict.
    """
    n = len(s) + 1
    dp = [False] * n
    dp[0] = True
    word_set = set(word_dict)
    for i in range(n):
        if dp[i]:
            for j in range(i + 1, n):
                if s[i:j] in word_set:
                    dp[j] = True
    return dp[-1]