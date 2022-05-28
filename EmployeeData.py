import csv
from datetime import date


def load_employee_data():
    """Saving a csv file as a list of dictionaries"""
    csv_file = open("/Users/sonmit01/Documents/Data/empData.csv")
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


def add_employee(name, gender):
    csv_file = open("/Users/sonmit01/Documents/Data/empData.csv", mode='r+', encoding='UTF8', newline='')
    csv_reader = csv.reader(csv_file)
    header = []
    header = next(csv_reader)
    today = date.today()
    today = today.strftime("%m/%d/%Y")
    record = {}
    emp_id = len(list(csv_reader)) + 1

    csvwriter = csv.DictWriter(csv_file, header)
    record[header[0]] = emp_id
    record[header[1]] = name
    record[header[2]] = today
    record[header[3]] = gender

    csvwriter.writerow(record)
