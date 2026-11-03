import csv

def parse_csv_line(line):
    reader = csv.reader(line.split(','))
    return list(next(reader))