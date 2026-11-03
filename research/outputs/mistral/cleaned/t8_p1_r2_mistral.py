import re

def validate_password(password):
    if len(password) < 8:
        return False
    lowercase = bool(re.search('[a-z]', password))
    uppercase = bool(re.search('[A-Z]', password))
    digit = bool(re.search('\\d', password))
    special_char = bool(re.search('[\\W_]', password))
    if not (lowercase and uppercase and digit and special_char):
        return False
    for i in range(1, len(password)):
        if password[i] == password[i - 1]:
            return False
    return True