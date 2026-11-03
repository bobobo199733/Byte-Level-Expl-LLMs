import json

def json_validator(text):
    """
    Validate whether a string contains syntactically valid JSON.

    Args:
        text (str): A string containing JSON data.

    Returns:
        bool: True if the input is syntactically valid JSON, False otherwise.
    """
    try:
        json.loads(text)
        return True
    except ValueError as e:
        print(f'Invalid JSON: {e}')
    return False