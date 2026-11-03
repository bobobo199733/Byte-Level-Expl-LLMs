def json_validator(text):
    """
    Checks if a given string contains valid JSON data.
    
    Args:
        text (str): The input string to check for valid JSON.
    
    Returns:
        bool: True if the string contains valid JSON, False otherwise.
    """
    try:
        json.loads(text)
        return True
    except ValueError:
        return False