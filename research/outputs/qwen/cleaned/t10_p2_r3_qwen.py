def longest_palindrome(s: str) -> str:

    def expand_around_center(left: int, right: int) -> str:
        while left >= 0 and right < len(s) and (s[left] == s[right]):
            left -= 1
            right += 1
        return s[left + 1:right]
    if not s:
        return ''
    result = ''
    for i in range(len(s)):
        palindrome_odd = expand_around_center(i, i)
        if len(palindrome_odd) > len(result):
            result = palindrome_odd
        palindrome_even = expand_around_center(i, i + 1)
        if len(palindrome_even) > len(result):
            result = palindrome_even
    return result