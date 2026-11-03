def longest_palindrome(s):
    if not s or len(s) <= 1:
        return s
    max_length = 1
    start = 0
    for i in range(len(s)):
        low = i - 1
        high = i + 1
        while low >= 0 and high < len(s) and (s[low] == s[high]):
            if high - low > max_length:
                start = i - (high - low) // 2
                max_length = high - low + 1
            low -= 1
            high += 1
        low = i - 1
        j = i + 1
        while low >= 0 and j < len(s) and (s[low] == s[j]):
            if j - low > max_length:
                start = i - (j - low) // 2
                max_length = j - low + 1
            low -= 1
            j += 1
    return s[start:start + max_length]