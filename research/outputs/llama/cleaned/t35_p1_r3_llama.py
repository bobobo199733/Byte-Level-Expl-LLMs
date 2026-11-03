def json_validator(text):
    """
    Validate if the provided text is a valid JSON string.

    Args:
        text (str): The input string to validate as JSON.

    Returns:
        bool: True if the input string contains valid JSON, False otherwise.
    """
    try:
        json.loads(text)
        return True
    except ValueError as e:
        print(f'Invalid JSON: {e}')
        return False