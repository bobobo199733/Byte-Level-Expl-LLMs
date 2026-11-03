def parse_csv_line(line):
    fields = []
    current_field = ''
    for char in line:
        if char == '"':
            if len(line) > 1 and line[1 + line.index(char)] == ',':
                current_field += char
                continue
            fields.append(current_field)
            current_field = ''
        elif char == ',':
            if current_field:
                fields.append(current_field.strip('"'))
                current_field = ''
            else:
                fields.append(char)
        else:
            current_field += char
    if current_field:
        fields.append(current_field)
    return fields