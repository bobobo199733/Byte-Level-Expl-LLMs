def parse_csv_line(line):
    """
    Splits a single CSV line into individual fields.

    Args:
        line (str): A string representing a CSV line.

    Returns:
        list: A list of strings where each element is a field from the input CSV line.
    """
    import csv
    reader = csv.reader([line])
    return next(reader)