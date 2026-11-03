import re

def validate_password(password):
    conditions = [len(password) >= 8, bool(re.search('[a-z]', password)), bool(re.search('[A-Z]', password)), bool(re.search('\\d', password)), bool(re.search('[!@#$%^&*(),.?":{}|<>]', password))]
    if all(conditions):
        return True
    else:
        return False