import re

def json_validator(text):
    json_elements = {'object': '{{(\\s*(?:"[^"]+"|\\d+\\.\\d+|\\d+|\\t|\\\\|,|{\\s.*\\s}|}\\s*,)*(\\s*\\}))', 'array': '(\\[\\s*(?:"[^"]+"|\\d+\\.\\d+|\\d+|\\t|\\\\|,|{|}\\s*,)*(\\s*\\]))', 'string': '"([^"\\\\]|\\\\.)*"', 'number': '(0|[1-9]\\d*)(\\.\\d+)?([eE][-+]?\\d+)?', 'boolean': 'true|false', 'null': 'null'}

    def find_all(pattern, string):
        return re.findall(pattern, string) if string else []
    valid = True
    for key, pattern in json_elements.items():
        matches = find_all(pattern, text)
        if not matches:
            return False
        for match in matches:
            if re.search('[^{}\\[\\]\\t"\\\\]+', match):
                valid = False
                break
    return valid