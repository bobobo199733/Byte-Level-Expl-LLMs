def word_break(s, word_dict):
    """
    Returns True if string s can be segmented into space-separated sequence of 
    one or more words from word_dict, False otherwise.

    :param s: input string to be segmented
    :type s: str
    :param word_dict: list of valid words
    :type word_dict: list[str]
    :return: whether string can be segmented
    :rtype: bool
    """
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True
    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_dict:
                dp[i] = True
                break
    return dp[n]