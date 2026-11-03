import re

def validate_password(password):
    if len(password) < 8:
        return False
    has_uppercase = re.search('[A-Z]', password)
    has_lowercase = re.search('[a-z]', password)
    has_digit = re.search('\\d', password)
    has_special_char = re.search('[^A-Za-z0-9]', password)
    return bool(has_uppercase and has_lowercase and has_digit and has_special_char)