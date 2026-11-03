def word_break(s: str, word_dict: list[str]) -> bool:
    """
    Checks if a given string can be segmented into words from a dictionary.

    Args:
        s (str): The input string to segment.
        word_dict (list[str]): A list of words that can be used for segmentation.

    Returns:
        bool: True if the string can be segmented, False otherwise.
    """
    dp = [False] * (len(s) + 1)
    dp[0] = True
    for i in range(1, len(s) + 1):
        for j in range(i):
            if s[j:i] in word_dict and dp[j]:
                dp[i] = True
    return dp[-1]