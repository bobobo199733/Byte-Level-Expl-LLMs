import re

def validate_password(password):
    """
    Validate a password based on the following rules:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character

    Args:
        password (str): The password to validate

    Returns:
        bool: True if the password is valid, False otherwise
    """
    pattern = '^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*#?&])[A-Za-z\\d@$!%*#?&]{8,}$'
    return bool(re.match(pattern, password))