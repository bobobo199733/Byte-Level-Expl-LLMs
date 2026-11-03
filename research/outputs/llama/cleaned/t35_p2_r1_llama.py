import json

def json_validator(text):
    """
    Validates whether a string contains syntactically valid JSON.

    Args:
        text (str): The input string to validate.

    Returns:
        bool: True if the string is valid JSON, False otherwise.
    """
    try:
        json.loads(text)
        return True
    except ValueError as e:
        if str(e):
            return False
        else:
            return False
    except Exception as e:
        raise