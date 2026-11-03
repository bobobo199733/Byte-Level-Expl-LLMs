def longest_palindrome(s):
    if not s:
        return ''
    max_length = 1
    start = 0
    for i in range(len(s)):
        left, right = (i, i)
        while left >= 0 and right < len(s) and (s[left] == s[right]):
            if right - left + 1 > max_length:
                start = left
                max_length = right - left + 1
            left -= 1
            right += 1
    for i in range(len(s)):
        left, right = (i, i + 1)
        while left >= 0 and right < len(s) and (s[left] == s[right]):
            if right - left + 1 > max_length:
                start = left
                max_length = right - left + 1
            left -= 1
            right += 1
    return s[start:start + max_length]