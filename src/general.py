import csv


def load_data(data_file):
    """
    Load data from CSV file
    :param data_file: csv file
    :return:
    """
    with open(data_file, 'r') as f:
        reader = csv.reader(f, skipinitialspace=True)
        data = [item for item in reader]
    return data[0]
