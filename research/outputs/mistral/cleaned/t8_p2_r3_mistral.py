import re

def validate_password(password):
    if len(password) < 8:
        return False
    has_upper = bool(re.search('[A-Z]', password))
    has_lower = bool(re.search('[a-z]', password))
    has_digit = bool(re.search('\\d', password))
    has_special = bool(re.search('[\\W\\_]', password))
    if not (has_upper and has_lower and has_digit and has_special):
        return False
    return True