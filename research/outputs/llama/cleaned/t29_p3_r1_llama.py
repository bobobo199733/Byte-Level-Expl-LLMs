def parse_csv_line(line):
    """
    Splits a CSV line into fields.

    Args:
        line (str): A string representing a single line of a CSV file.

    Returns:
        list: A list of strings where each string is a field from the CSV line.
    """
    return line.split(',')