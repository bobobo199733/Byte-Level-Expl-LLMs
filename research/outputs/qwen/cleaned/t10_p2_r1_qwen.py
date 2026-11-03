def longest_palindrome(s: str) -> str:

    def expand_around_center(left: int, right: int) -> str:
        while left >= 0 and right < len(s) and (s[left] == s[right]):
            left -= 1
            right += 1
        return s[left + 1:right]
    if not s:
        return ''
    max_palindrome = ''
    for i in range(len(s)):
        palindrome1 = expand_around_center(i, i)
        palindrome2 = expand_around_center(i, i + 1)
        if len(palindrome1) > len(max_palindrome):
            max_palindrome = palindrome1
        if len(palindrome2) > len(max_palindrome):
            max_palindrome = palindrome2
    return max_palindrome