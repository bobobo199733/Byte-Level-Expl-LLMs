def longest_palindrome(s):
    """
    Returns the longest palindromic substring in a given string s.
    
    If there are multiple valid answers with the same maximum length, 
    return any one of them.
    
    :param s: Input string.
    :return: Longest palindromic substring.
    """

    def expand_around_center(s, left, right):
        """
        Helper function to expand around a given center point in a string s.
        
        This function returns the longest palindrome centered at (left, right) 
        in the string s. It expands outward from the center as long as it can, 
        returning the first palindromic substring found that is not equal to 
        one character.
        
        :param s: Input string.
        :param left: Left boundary of palindrome substring.
        :param right: Right boundary of palindrome substring.
        :return: Longest palindromic substring centered at (left, right) in s.
        """
        while left >= 0 and right < len(s) and (s[left] == s[right]):
            left -= 1
            right += 1
        return s[left + 1:right]
    longest = ''
    for i in range(len(s)):
        odd_palindrome = expand_around_center(s, i, i)
        even_palindrome = expand_around_center(s, i, i + 1)
        if len(odd_palindrome) > len(longest):
            longest = odd_palindrome
        if len(even_palindrome) > len(longest):
            longest = even_palindrome
    return longest