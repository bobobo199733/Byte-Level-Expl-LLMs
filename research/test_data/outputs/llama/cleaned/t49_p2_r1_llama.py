def word_break(s, word_dict):
    """
    Determine if a given string can be segmented into words from a dictionary.

    Args:
        s (str): The input string to segment.
        word_dict (list[str]): A list of valid words.

    Returns:
        bool: Whether the string can be segmented into words from the dictionary.
    """
    word_set = set(word_dict)
    dp = [False] * (len(s) + 1)
    dp[0] = True
    for i in range(1, len(s) + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_set:
                dp[i] = True
    return dp[-1]