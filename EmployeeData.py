import csv
from datetime import date
import CommonFunctions as cf
import UpdateData as ud

data_file = "/Users/sonmit01/Documents/Data/empData.csv"


def load_employee_data():
    """Saving employee data csv file as a list of dictionaries"""
    list_data = cf.csv_to_dict(data_file)

    return list_data


def add_employee(name, gender):
    """Adding a new employee to the database"""
    csv_file = open(data_file, mode='r+', encoding='UTF8', newline='')
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
    ud.add_employee(record)
