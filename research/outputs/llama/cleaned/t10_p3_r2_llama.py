def longest_palindrome(s: str) -> str:
    """
    Returns the longest palindromic substring in a given string.

    Args:
        s (str): The input string.

    Returns:
        str: The longest palindromic substring.
    """

    def expand_around_center(left, right):
        while left >= 0 and right < len(s) and (s[left] == s[right]):
            left -= 1
            right += 1
        return s[left + 1:right]
    if not s:
        return ''
    longest = ''
    for i in range(len(s)):
        odd_palindrome = expand_around_center(i, i)
        if len(odd_palindrome) > len(longest):
            longest = odd_palindrome
        even_palindrome = expand_around_center(i, i + 1)
        if len(even_palindrome) > len(longest):
            longest = even_palindrome
    return longest