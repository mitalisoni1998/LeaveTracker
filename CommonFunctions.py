import csv
from datetime import datetime
import Constants
import logging


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


def verify_weekend_holiday(date):
    current_date = (datetime.strptime(date, '%m/%d/%Y')).date()
    current_date_str = current_date.strftime('%Y-%m-%d')
    if current_date_str in Constants.get_public_holidays():
        return True
    elif current_date.weekday() > 4:
        return True
    else:
        return False

