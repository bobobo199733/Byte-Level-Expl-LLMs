def parse_csv_line(line):
    """
    Parse one CSV row.

    Args:
        line (str): A single line of a CSV file.

    Returns:
        list: The parsed row as a list of strings, with commas separating fields and quotes removed from quoted fields.
    """
    result = []
    current_field = ''
    in_quotes = False
    for char in line:
        if char == '"':
            in_quotes = not in_quotes
        elif char == ',' and (not in_quotes):
            result.append(current_field)
            current_field = ''
        else:
            current_field += char
    result.append(current_field)
    return [field.strip('"') for field in result if field]