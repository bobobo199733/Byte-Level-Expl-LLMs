import re

def validate_password(password):
    MIN_LENGTH = 8
    if len(password) < MIN_LENGTH:
        return False
    has_uppercase = bool(re.search('[A-Z]', password))
    has_lowercase = bool(re.search('[a-z]', password))
    has_digit = bool(re.search('\\d', password))
    has_special_char = bool(re.search('[^A-Za-z0-9]', password))
    if not (has_uppercase and has_lowercase and has_digit and has_special_char):
        return False
    return True