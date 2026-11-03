def validate_password(password):
    if len(password) < 8:
        return False
    has_uppercase = any((c.isupper() for c in password))
    has_lowercase = any((c.islower() for c in password))
    has_digit = any((c.isdigit() for c in password))
    has_special_char = any((not c.isalnum() for c in password))
    return has_uppercase and has_lowercase and has_digit and has_special_char