import re

def validate_password(password):
    """
    Validate a password based on the following rules:
     - At least 8 characters long
     - At most 128 characters long
     - Contains at least one lowercase letter
     - Contains at least one uppercase letter
     - Contains at least one digit
     - Does not contain any whitespace

    Args:
        password (str): The password to validate.

    Returns:
        bool: True if the password is valid, False otherwise.
    """
    pattern = re.compile('^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?!.*\\s).{8,128}$')
    return bool(pattern.match(password))