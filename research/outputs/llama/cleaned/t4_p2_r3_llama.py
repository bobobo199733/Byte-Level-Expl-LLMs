def decode_string(s: str) -> str:
    """
    This function decodes a string s with encoded characters, replacing each encoded character
    with its actual value. The encoding syntax is 'num[c]' where num is a decimal number and c
    is any character.
    
    :param s: The input string to be decoded.
    :return: The decoded string.
    """
    stack = []
    curNum = 0
    prevChar = ''
    for i in range(len(s)):
        if s[i].isdigit():
            curNum = curNum * 10 + int(s[i])
        elif s[i] == '[':
            stack.append((prevChar, curNum))
            prevChar = ''
            curNum = 0
        elif s[i] == ']':
            num, char = stack.pop()
            prevChar = char * curNum + prevChar
            curNum = num
        else:
            prevChar += s[i]
    return prevChar