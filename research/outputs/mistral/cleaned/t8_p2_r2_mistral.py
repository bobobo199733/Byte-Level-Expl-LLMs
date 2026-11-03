import re

def validate_password(password):
    if len(password) < 8:
        return False
    if not re.search('[A-Z]', password):
        return False
    if not re.search('[a-z]', password):
        return False
    if not re.search('\\d', password):
        return False
    if not re.search('[\\W_]', password):
        return False
    return True