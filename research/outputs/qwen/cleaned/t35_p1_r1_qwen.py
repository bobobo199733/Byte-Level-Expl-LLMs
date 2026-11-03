def json_validator(text):
    try:
        import json
        json.loads(text)
        return True
    except ValueError:
        return False