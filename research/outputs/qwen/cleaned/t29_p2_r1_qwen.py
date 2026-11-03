def parse_csv_line(line):
    if line[0] != '"':
        return [field.strip() for field in line.split(',')]
    quote, fields = (True, [])
    field = ''
    for char in line[1:]:
        if char == '"' and quote:
            quote = False
            continue
        elif char == ',' and (not quote):
            fields.append(field.strip())
            field = ''
            continue
        field += char
    fields.append(field.strip() if field else '')
    return fields[:-1] if fields[-1] == '' else fields