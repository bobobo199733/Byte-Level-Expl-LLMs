def word_break(s, word_dict):
    """
    Returns True if s can be segmented into a space-separated sequence of one or more dictionary words, False otherwise.
    
    :param s: string to be segmented
    :type s: str
    :param word_dict: list of strings (dictionary)
    :type word_dict: list[str]
    :return: True if s can be segmented, False otherwise
    :rtype: bool
    """
    dp = [False] * (len(s) + 1)
    dp[0] = True
    for i in range(1, len(s) + 1):
        for j in range(i):
            if dp[j] and s[j:i] in word_dict:
                dp[i] = True
                break
    return dp[-1]