import re

def validate_password(password):
    if len(password) < 8:
        return False
    has_uppercase = bool(re.search('[A-Z]', password))
    has_lowercase = bool(re.search('[a-z]', password))
    has_digit = bool(re.search('\\d', password))
    has_special = bool(re.search('[\\W_]', password))
    if not (has_uppercase and has_lowercase and has_digit and has_special):
        return False
    return True