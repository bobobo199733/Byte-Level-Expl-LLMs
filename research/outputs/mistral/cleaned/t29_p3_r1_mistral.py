import csv

def parse_csv_line(line):
    return list(csv.reader([line], delimiter=','))[0]