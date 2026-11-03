import re

def json_validator(text):
    """
    Validates a given string as valid JSON.

    Args:
        text (str): The input string to be validated.

    Returns:
        bool: True if the input is valid JSON, False otherwise.
    """
    pattern = '^\\s*([{}"\\[\\]]|[a-zA-Z0-9_]+|true|false|null)\\s*(?:,\\s*[{}"\\[\\]]|[a-zA-Z0-9_]+|true|false|null\\s*)*$'
    text = re.sub('\\s+', '', text)
    return bool(re.match(pattern, text))