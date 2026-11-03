import re

def validate_password(password):
    """
    Validate a password based on the following rules:
        - At least 8 characters long
        - Contains at least one uppercase letter
        - Contains at least one lowercase letter
        - Contains at least one digit
        - Does not contain any whitespace
        - Does not match a common password

    Returns True if the password is strong, False otherwise.
    """
    common_passwords = ['password123', 'qwerty', 'letmein']
    if len(password) < 8 or any((char.isspace() for char in password)):
        return False
    has_uppercase = re.search('[A-Z]', password)
    has_lowercase = re.search('[a-z]', password)
    has_digit = re.search('\\d', password)
    if not (has_uppercase and has_lowercase and has_digit):
        return False
    for common_password in common_passwords:
        if password == common_password:
            return False
    return True