import re

def validate_password(password: str) -> bool:
    """
    Validate the strength of a password.
    
    A strong password is considered to be at least 8 characters long, containing 
    at least one uppercase letter, one lowercase letter, one digit and one special character.
    
    Parameters:
    password (str): The password to validate
    
    Returns:
    bool: True if the password is strong, False otherwise
    """
    uppercase_pattern = '[A-Z]'
    lowercase_pattern = '[a-z]'
    digit_pattern = '\\d'
    special_character_pattern = "[!@#$%^&*()_+=-{};:'<>,./?]"
    if len(password) < 8:
        return False
    if not (re.search(uppercase_pattern, password) and re.search(lowercase_pattern, password) and re.search(digit_pattern, password) and re.search(special_character_pattern, password)):
        return False
    return True