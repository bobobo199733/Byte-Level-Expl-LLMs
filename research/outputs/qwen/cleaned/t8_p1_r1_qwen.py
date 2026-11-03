def validate_password(password):
    """
    Validates a given password according to specific criteria:
    
    - Password length should be at least 8 characters.
    - Password should contain at least one uppercase letter.
    - Password should contain at least one lowercase letter.
    - Password should contain at least one digit.

    Args:
        password (str): The password to validate.

    Returns:
        bool: True if the password is valid, False otherwise.
    """
    if len(password) < 8:
        return False
    has_uppercase = any((c.isupper() for c in password))
    has_lowercase = any((c.islower() for c in password))
    has_digit = any((c.isdigit() for c in password))
    return has_uppercase and has_lowercase and has_digit