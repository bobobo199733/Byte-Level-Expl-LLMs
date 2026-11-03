def longest_palindrome(s):
    """
    Returns the longest substring of s that is a palindrome.

    :param s: The input string.
    :return: The longest substring of s that is a palindrome.
    """

    def expand_around_center(s, left, right):
        while left >= 0 and right < len(s) and (s[left] == s[right]):
            left -= 1
            right += 1
        return s[left + 1:right]
    if not s:
        return ''
    longest = ''
    for i in range(len(s)):
        odd_palindrome = expand_around_center(s, i, i)
        even_palindrome = expand_around_center(s, i, i + 1)
        if len(odd_palindrome) > len(longest):
            longest = odd_palindrome
        if len(even_palindrome) > len(longest):
            longest = even_palindrome
    return longest