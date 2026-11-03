import re

def json_validator(text):
    """
    Check if the input string contains valid JSON.

    Args:
        text (str): The string to be validated as JSON.

    Returns:
        bool: True if the string is a valid JSON, False otherwise.
    """
    try:
        json.loads(text)
    except ValueError:
        return False
    return True