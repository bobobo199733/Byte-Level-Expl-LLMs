def longest_palindrome(s):
    if len(s) == 0:
        return ''
    max_length = 1
    start_index = 0
    for i in range(len(s)):
        low, high = (i, i)
        while low >= 0 and high < len(s) and (s[low] == s[high]):
            if high - low + 1 > max_length:
                start_index = low
                max_length = high - low + 1
            low -= 1
            high += 1
        low, high = (i, i + 1)
        while low >= 0 and high < len(s) and (s[low] == s[high]):
            if high - low + 1 > max_length:
                start_index = low + 1
                max_length = high - low + 1
            low -= 1
            high += 1
    return s[start_index:start_index + max_length]