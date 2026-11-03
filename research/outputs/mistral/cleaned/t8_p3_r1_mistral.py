import re

def validate_password(password):
    if len(password) < 8:
        return False
    if not re.search('[A-Z]', password):
        return False
    if not re.search('[a-z]', password):
        return False
    if not re.search('[0-9]', password):
        return False
    if not re.search('[!@#$%^&*(),.?":{}|<>]', password):
        return False
    return True