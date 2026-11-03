import re

def validate_password(password):
    if len(password) < 8:
        return False
    if not re.search('[A-Z]', password) or not re.search('[a-z]', password) or (not re.search('\\d', password)):
        return False
    if not re.search('[\\W]', password):
        return False
    return True