def parse_csv_line(line):
    result = []
    field = ''
    in_quote = False
    for char in line:
        if char == '"':
            in_quote = not in_quote
        elif char == ',' and (not in_quote):
            result.append(field)
            field = ''
        else:
            field += char
    if field:
        result.append(field)
    return result