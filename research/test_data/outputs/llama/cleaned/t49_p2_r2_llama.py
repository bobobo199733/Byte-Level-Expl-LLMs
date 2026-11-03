def word_break(s, word_dict):
    """
    Returns whether s can be segmented into words from word_dict.

    Args:
        s (str): The input string to segment.
        word_dict (list[str]): List of words that can be used for segmentation.

    Returns:
        bool: Whether s can be segmented using words from word_dict.
    """
    word_set = set(word_dict)
    dp = [False] * (len(s) + 1)
    dp[0] = True
    for i in range(1, len(s) + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
                break
    return dp[len(s)]