import re

def json_validator(text):
    """
    Validates if a given string is valid JSON.

    Args:
        text (str): The input string to validate as JSON.

    Returns:
        bool: True if the string is valid JSON, False otherwise.
    """
    json_pattern = '^(\\s*(?:true|false|null|[-+]?[\\d.]+(?:e[-+]?\\d+)?|\\{.*?\\}|\\[.*?\\])\\s*)*$'
    return bool(re.match(json_pattern, text))