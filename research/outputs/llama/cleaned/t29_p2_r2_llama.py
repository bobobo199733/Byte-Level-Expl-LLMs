def parse_csv_line(line):
    result = []
    current_field = ''
    in_quote = False
    for char in line:
        if char == '"':
            in_quote = not in_quote
        elif char == ',' and (not in_quote):
            result.append(current_field)
            current_field = ''
        else:
            current_field += char
    result.append(current_field)
    return [None if field == '' else field for field in result]