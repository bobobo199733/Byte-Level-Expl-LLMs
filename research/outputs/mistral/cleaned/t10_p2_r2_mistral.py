def longest_palindrome(s):
    if not s:
        return ''
    max_length = 1
    start = 0
    for i in range(len(s)):
        odd_half = s[i:i + max_length + 1]
        if len(odd_half) > max_length and all((ch == odd_half[0] for ch in odd_half[1:])):
            start = i
            max_length += 2
        for j in range(i - max_length, i):
            even_half = s[j:i + 1][::-1] + s[i:i + max_length + 1]
            if len(even_half) > max_length and all((ch == ch2 for ch, ch2 in zip(even_half, even_half[1:]))):
                start = j
                max_length += 2
    return s[start:start + max_length]