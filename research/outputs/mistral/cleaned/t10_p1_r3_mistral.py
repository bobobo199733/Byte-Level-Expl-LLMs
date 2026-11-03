def longest_palindrome(s):
    if len(s) == 0:
        return ''
    max_length = 1
    start_index = 0
    for i in range(len(s)):
        left, right = (i, i)
        while left >= 0 and right < len(s) and (s[left] == s[right]):
            if right - left + 1 > max_length:
                start_index = left
                max_length = right - left + 1
            left -= 1
            right += 1
        left, right = (i - 1, i + 1)
        while left >= 0 and right < len(s) and (s[left] == s[right]):
            if right - left + 1 > max_length:
                start_index = left - 1
                max_length = right - left + 2
            left -= 1
            right += 1
    return s[start_index:start_index + max_length]