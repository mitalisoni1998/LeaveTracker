import UpdateData as ud
import CommonFunctions as cf
import schedule
import csv
from datetime import date
import time

data_file = "/Users/sonmit01/Documents/Data/EmployeeLeaveData.csv"


def log_compoff(emp_id, dates):
    """To log extra days of work"""
    list_dates = list(dates)
    valid_compoff = 0
    for date_value in list_dates:
        if cf.verify_weekend_holiday(date_value):
            print("Compoff added for: ", date_value)
            valid_compoff += 1
        else:
            continue
    ud.add_compoff(emp_id, valid_compoff)
    print("Valid extra days were {} and comp off has been added for them!".format(valid_compoff))


def add_ooo_leaves():
    """To add accrued leaves every month"""
    list_data = cf.csv_to_dict(data_file)
    today = date.today()
    current_month = today.strftime("%b")
    last_update_date = list_data[0].get('OooUpdateDate')
    if current_month == 'Jan':
        for record in list_data:
            ooo_leaves = int(record['OooLeaves'])
            if ooo_leaves < 39:
                ooo_leaves += 2
                record['OooLeaves'] = ooo_leaves
                record['OooUpdateDate'] = today
            else:
                record['OooLeaves'] = 40
                record['OooUpdateDate'] = today
    else:
        for record in list_data:
            ooo_leaves = int(record['OooLeaves'])
            ooo_leaves += 2
            record['OooLeaves'] = ooo_leaves
            record['OooUpdateDate'] = today

    list_keys = list(list_data[0].keys())
    csv_file = open(data_file, mode='r+', encoding='UTF8', newline='')
    csv_file.truncate()
    csvwriter = csv.DictWriter(csv_file, list_keys)
    csvwriter.writeheader()
    for updated_record in list_data:
        csvwriter.writerow(updated_record)




