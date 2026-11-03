import re

def validate_password(password):
    """
    Validate a password based on several criteria.

    Args:
        password (str): The password to be validated.

    Returns:
        bool: True if the password is valid, False otherwise.
    """
    has_upper = re.search('[A-Z]', password)
    has_lower = re.search('[a-z]', password)
    has_digit = re.search('\\d', password)
    has_special = re.search('[^A-Za-z0-9]', password)
    return len(password) >= 8 and has_upper and has_lower and has_digit and has_special