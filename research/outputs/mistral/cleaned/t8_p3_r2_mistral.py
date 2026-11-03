import re

def validate_password(password):
    if len(password) < 8:
        return False
    lowercase = re.search('[a-z]', password)
    uppercase = re.search('[A-Z]', password)
    digit = re.search('[0-9]', password)
    special_char = re.search('[!@#$%^&*(),.?/:;{}|<>]', password)
    if not (lowercase and uppercase and digit and special_char):
        return False
    for char in password:
        if char.isalpha() or char.isdigit() or char.isalnum(char) or char.isspace():
            continue
        count = password.count(char)
        if count < 2:
            return False
    return True