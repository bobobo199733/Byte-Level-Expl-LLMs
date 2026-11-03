def parse_csv_line(line):
    if line.startswith('"') and line.endswith('"'):
        line = line[1:-1]
    return [f.strip().strip('"') for f in line.split(',') if f]