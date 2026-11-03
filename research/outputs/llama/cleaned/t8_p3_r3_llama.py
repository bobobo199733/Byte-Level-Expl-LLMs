import re

def validate_password(password):
    """
    Check if a password is strong.

    A strong password must have:
        * Minimum length of 8 characters
        * At least one uppercase letter
        * At least one lowercase letter
        * At least one digit
        * At least one special character

    Args:
        password (str): The password to validate.

    Returns:
        bool: True if the password is strong, False otherwise.
    """
    pattern = re.compile('(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@#$%^&+=]).{8,}')
    return bool(pattern.match(password))