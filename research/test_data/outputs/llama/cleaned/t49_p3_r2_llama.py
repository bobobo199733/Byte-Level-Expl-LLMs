def word_break(s: str, word_dict: list[str]) -> bool:
    """
    Return True if the string s can be built by concatenating words from word_dict,
    False otherwise.

    :param s: input string
    :type s: str
    :param word_dict: dictionary of valid words
    :type word_dict: list[str]
    :return: True if s can be formed, False otherwise
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