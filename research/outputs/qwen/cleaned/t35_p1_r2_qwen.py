import json

def json_validator(text):
    try:
        json.loads(text)
        return True
    except ValueError:
        return False