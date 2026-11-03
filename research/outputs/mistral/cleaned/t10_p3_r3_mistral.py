def longest_palindrome(s):
    if len(s) == 0:
        return ''
    max_length = 1
    start_index = 0
    for i in range(len(s)):
        temp = s[i:i + max_length + 1]
        if len(temp) > max_length and temp == temp[::-1]:
            start_index = i
            max_length = len(temp)
        for j in range(i + 1, len(s)):
            temp = s[i:j + 1]
            if len(temp) > max_length and temp == temp[::-1]:
                start_index = i
                max_length = len(temp)
    return s[start_index:start_index + max_length]