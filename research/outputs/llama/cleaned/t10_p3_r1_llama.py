def longest_palindrome(s: str) -> str:

    def expand_around_center(left, right):
        while left >= 0 and right < len(s) and (s[left] == s[right]):
            left -= 1
            right += 1
        return s[left + 1:right]
    max_length = 0
    start = 0
    for i in range(len(s)):
        odd_len = expand_around_center(i, i)
        even_len = expand_around_center(i, i + 1)
        if len(odd_len) > len(even_len):
            temp_start, temp_end = (i, i + len(odd_len))
            max_length = max(max_length, len(odd_len))
            start = min(start, temp_start)
        else:
            temp_start, temp_end = (i, i + 1 + len(even_len))
            max_length = max(max_length, len(even_len))
            start = min(start, temp_start)
    return s[start:start + max_length]