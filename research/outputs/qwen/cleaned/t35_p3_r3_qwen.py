def json_validator(text):
    # Helper functions to parse JSON
    def parse_value(s, i):
        if s[i] == '"':
            return parse_string(s, i + 1)
        elif s[i:i+4] == 'null' or s[i:i+5] == 'false' or s[i:i+4] == 'true':
            return s[i:i+4].lower() if s[i:i+4] in ('null', 'false') else s[i:i+5].lower(), i + 4
        elif s[i] == '[':
            return parse_array(s, i)
        elif s[i] == '{':
            return parse_object(s, i)
        elif s[i].isdigit() or (s[i] in '+-' and s[i + 1].isdigit()):
            end = i + 1
            while end < len(s) and (s[end].isdigit() or s[end] in '.-'):
                end += 1
            return float(s[i:end]) if '.' in s[i:end] else int(s[i:end]), end - 1

    def parse_string(s, i):
        result = []
        while True:
            ch = s[i]
            if ch == '\\':
                i += 1
                escape_char = s[i]
                if escape_char == 'u':  # Unicode escape sequence
                    i += 4
                else:
                    result.append(escape_char)
            elif ch == '"':
                return ''.join(result), i + 1
            else:
                result.append(ch)
            i += 1

    def parse_array(s, i):
        array = []
        while True:
            if s[i] == ']':
                return array, i + 1
            value, i = parse_value(s, i)
            array.append(value)

    def parse_object(s, i):
        obj = {}
        while True:
            key, i = parse_string(s, i)
            if s[i] != ':':
                raise ValueError(f"Invalid JSON: Expected ':' but found {s[i]}")
            value, i = parse_value(s, i + 1)
            obj[key] = value
            if s[i] == '}':
                return obj, i + 1

    # Start parsing from the beginning of the string
    try:
        result, _ = parse_object(text, 0)
        return True
    except (ValueError, IndexError):
        return False

# Example usage
print(json_validator('{"name": "John", "age": 30}'))  # Should print: True
print(json_validator('[1, 2, 3, "abc"]'))             # Should print: True
print(json_validator('{"name": John}')                 # Should print: False