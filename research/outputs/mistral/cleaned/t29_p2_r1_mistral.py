def parse_csv_line(line):
    fields = []
    field = ''
    is_quoted = False
    for char in line:
        if char == '"':
            is_quoted = not is_quoted
        elif char == ',' and (not is_quoted or char != line[-1]) and (len(field) > 0):
            fields.append(field)
            field = ''
        else:
            field += char
    if len(field) > 0:
        fields.append(field)
    return fields