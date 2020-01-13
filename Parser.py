import csv

FILE_NAME = 'data/telemetry.csv'


def telemetry(file_name):
    file = open(file_name, "r")
    reader = csv.reader(file)
    for line in reader:
        t = line[1], line[2]
        print(t)


if __name__ == '__main__':
    telemetry(FILE_NAME)