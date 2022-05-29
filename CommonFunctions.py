import csv


def csv_to_dict(file):
    """Saving a csv file as a list of dictionaries"""
    csv_file = open(file)
    csv_reader = csv.reader(csv_file)
    header = []
    header = next(csv_reader)
    list_data = []
    for row in csv_reader:
        current_row = []
        current_row = row
        dict_row = {}
        for i in range(len(header)):
            dict_row[header[i]] = current_row[i]
        list_data.append(dict_row)

    return list_data
