def parse_csv_line(line):
    current_field = ''
    in_quotes = False
    result = []
    for char in line:
        if char == '"':
            in_quotes = not in_quotes
        elif char == ',' and (not in_quotes):
            result.append(current_field)
            current_field = ''
        else:
            current_field += char
    if in_quotes or current_field != '':
        result.append(current_field)
    return result