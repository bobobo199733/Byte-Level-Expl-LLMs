def parse_csv_line(line):
    """
    Splits a single line from a CSV file into its constituent fields.

    Args:
        line (str): A string representing one line from a CSV file.

    Returns:
        list: A list of strings, each representing a field in the CSV line.
    """
    import csv
    reader = csv.reader([line])
    return next(reader)