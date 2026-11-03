def wildcard_match(s: str, p: str) -> bool:
    """
    Returns True if the entire string s matches the wildcard pattern p, otherwise returns False.

    Rules:
    - '?' matches exactly one character
    - '*' matches any sequence of characters, including the empty sequence
    - Matching must cover the entire string

    :param s: The input string to match.
    :param p: The wildcard pattern to match against.
    :return: True if the string matches the pattern, False otherwise.
    """
    if not s and (not p):
        return True
    if p and p[0] == '*':
        return wildcard_match(s, p[1:]) or (s and wildcard_match(s[1:], p))
    if p and len(p) > 0 and (len(s) > 0) and (p[0] != s[0] and p[0] != '?'):
        return False
    if p and len(p) > 0 and (p[0] == s[0] or p[0] == '?'):
        return wildcard_match(s[1:], p[1:])
    return False