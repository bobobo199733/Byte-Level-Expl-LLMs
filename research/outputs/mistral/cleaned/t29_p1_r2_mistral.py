def parse_csv_line(line):
    return list(map(str.strip, line.split(',')))