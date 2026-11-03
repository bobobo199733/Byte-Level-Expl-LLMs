import re

def validate_password(password):
    if len(password) < 8:
        return False
    pattern = '^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*#?&])[A-Za-z\\d@$!%*#?&]{8,}$'
    if re.match(pattern, password):
        return True
    else:
        return False