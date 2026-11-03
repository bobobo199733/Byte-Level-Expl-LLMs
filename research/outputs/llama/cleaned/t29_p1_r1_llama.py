def parse_csv_line(line: str) -> list[str]:
    return [field.strip() for field in line.split(',')]