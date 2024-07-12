import csv

def read_csv(file_path):
    """
    Reads data from a .csv file and returns it as a list of dictionaries.
    Each dictionary represents a row in the .csv file.
    """
    data = []
    with open(file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

def write_csv(file_path, data, fieldnames):
    """
    Writes data to a .csv file.
    `data` should be a list of dictionaries, where each dictionary represents a row.
    `fieldnames` should be a list of column names.
    """
    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)