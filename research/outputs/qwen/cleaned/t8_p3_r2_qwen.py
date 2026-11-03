import re

def validate_password(password):
    MIN_LENGTH = 8
    if len(password) < MIN_LENGTH:
        return False
    if not re.search('[0-9]', password):
        return False
    if not re.search('[A-Z]', password):
        return False
    if not re.search('[a-z]', password):
        return False
    if not re.search('[^A-Za-z0-9]', password):
        return False
    return True