def validate_password(password):
    if len(password) < 8:
        return False
    has_uppercase = any((char.isupper() for char in password))
    has_lowercase = any((char.islower() for char in password))
    has_digit = any((char.isdigit() for char in password))
    has_special_char = any((char in '!@#$%^&*()-_=+[]{}|;:,.<>?/~' for char in password))
    return has_uppercase and has_lowercase and has_digit and (has_special_char if 'special_chars' in locals() else True)