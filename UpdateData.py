import csv
from datetime import datetime
import schedule
import EmployeeData as ed
from datetime import date
from datetime import datetime
import CommonFunctions as cf
import logging
from datetime import timedelta
import json
import ast
import sys

data_file = "/Users/sonmit01/Documents/Data/EmployeeLeaveData.csv"


def create_db():
    """Creating a csv file to act as a database for the employee leave data"""

    header = ['empId', 'Name', 'JoiningDate', 'Gender', 'OooLeaves', 'CompOff', 'Paternity', 'Maternity',
              'FlagMaternity', 'FlagPaternity',
              'FlagLeaveApplied', 'LeaveAppliedFrom', 'LeaveAppliedTo', 'NoOfLeavesApplied']

    list_empdata = ed.load_employee_data()
    csv_file = open(data_file, mode='w')
    csv_file = open(data_file, mode='r+', encoding='UTF8', newline='')
    csv_reader = csv.reader(csv_file)
    csvwriter = csv.DictWriter(csv_file, header)
    csvwriter.writeheader()
    is_empty = len(list(csv_reader))

    # if csv file is empty initial data should be populated
    if not is_empty:
        for record in list_empdata:
            record_leave = {'empId': record['empId'], 'Name': record['Name'], 'JoiningDate': record['JoiningDate'],
                            'Gender': record['Gender']}
            if record_leave['Gender'] == 'F':
                record_leave['Paternity'] = 0
                record_leave['Maternity'] = 28
            else:
                record_leave['Paternity'] = 168
                record_leave['Maternity'] = 0
            record_leave['CompOff'] = ''
            record_leave['FlagMaternity'] = False
            record_leave['FlagPaternity'] = False
            record_leave['FlagLeaveApplied'] = False
            record_leave['LeaveAppliedFrom'] = ''
            record_leave['LeaveAppliedTo'] = ''
            record_leave['NoOfLeavesApplied'] = 0

            ooo_leaves = get_no_of_months(record_leave['JoiningDate']) * 2
            if ooo_leaves > 40:
                ooo_leaves = 40

            record_leave['OooLeaves'] = ooo_leaves

            # write record into csv file
            csvwriter.writerow(record_leave)


def get_no_of_months(start_dt):
    """To calculate number of months between joining date and today"""
    today = date.today()
    today = today.strftime("%m/%d/%Y")
    today = datetime.strptime(today, "%m/%d/%Y")
    start = datetime.strptime(start_dt, "%m/%d/%Y")
    diff = (today.year - start.year) * 12 + (today.month - start.month)
    return diff


def add_compoff(emp_id, no_of_days):
    """To add compoff leaves when applied"""
    list_data = cf.csv_to_dict(data_file)

    today = date.today()
    today = today.strftime("%Y/%m/%d")
    today = (datetime.strptime(today, "%Y/%m/%d")).date()
    expiration = today + timedelta(days=30)
    expiration_dt = expiration.strftime("%m/%d/%Y")

    for record in list_data:
        is_present = False
        if record['empId'] == str(emp_id):
            if record['CompOff'] == '':
                dict_compoff = {expiration_dt: no_of_days}
                is_present = True
                record['CompOff'] = dict_compoff
                break
            else:
                dict_compoff = ast.literal_eval(record['CompOff'])
                if expiration_dt in dict_compoff.keys():
                    dict_compoff[expiration_dt] = int(dict_compoff[expiration_dt]) + no_of_days
                    is_present = True
                    record['CompOff'] = json.dumps(dict_compoff)  # Converts dict to string
                    break
                else:
                    dict_compoff[expiration_dt] = no_of_days
                    is_present = True
                    record['CompOff'] = json.dumps(dict_compoff)
                    break

    if not is_present:
        logging.exception("EmpId {} not found!".format(emp_id))
        sys.exit()

    list_keys = list(list_data[0].keys())
    csv_file = open(data_file, mode='r+', encoding='UTF8', newline='')
    csv_file.truncate()
    csvwriter = csv.DictWriter(csv_file, list_keys)
    csvwriter.writeheader()
    for updated_record in list_data:
        csvwriter.writerow(updated_record)


def remove_compoff(emp_id, no_of_days, start_dt, end_dt):
    """To remove compoff leaves when applied"""
    list_data = cf.csv_to_dict(data_file)

    start = (datetime.strptime(start_dt, "%m/%d/%Y")).date()
    end = (datetime.strptime(end_dt, "%m/%d/%Y")).date()

    for record in list_data:
        is_present = False
        if record['empId'] == str(emp_id):
            is_present = True
            dict_compoff = ast.literal_eval(record['CompOff'])  # Convert dictionary string to a dictionary object
            dict_compoff_keys = list(dict_compoff.keys())
            if len(dict_compoff) == 1:
                compoff_available = int(dict_compoff[dict_compoff_keys[0]])
                if compoff_available >= no_of_days:
                    dict_compoff[dict_compoff_keys[0]] = compoff_available - no_of_days
                    record['LeaveAppliedFrom'] = start
                    record['LeaveAppliedTo'] = end
                    record['FlagLeaveApplied'] = True
                    record['CompOff'] = dict_compoff
                else:
                    return False
            else:
                compoff_available = 0
                for key in dict_compoff_keys:
                    compoff_available += int(dict_compoff[key])
                if compoff_available >= no_of_days:
                    dict_compoff_keys.sort(key=lambda d: datetime.strptime(d, "%m/%d/%Y"))
                    counter = no_of_days
                    for key in dict_compoff_keys:
                        compoff_available = int(dict_compoff[key])
                        if counter > 0:
                            if compoff_available >= no_of_days:
                                dict_compoff[key] = compoff_available - no_of_days
                                counter -= no_of_days
                                record['LeaveAppliedFrom'] = start
                                record['LeaveAppliedTo'] = end
                                record['FlagLeaveApplied'] = True
                                record['CompOff'] = dict_compoff
                            else:
                                dict_compoff[key] = 0
                                counter = counter - compoff_available
                                record['LeaveAppliedFrom'] = start
                                record['LeaveAppliedTo'] = end
                                record['FlagLeaveApplied'] = True
                                record['CompOff'] = dict_compoff
                        else:
                            break

                else:
                    return False

    if not is_present:
        logging.exception("EmpId {} not found!".format(emp_id))
        sys.exit()

    list_keys = list(list_data[0].keys())
    csv_file = open(data_file, mode='r+', encoding='UTF8', newline='')
    csv_file.truncate()
    csvwriter = csv.DictWriter(csv_file, list_keys)
    csvwriter.writeheader()
    for updated_record in list_data:
        csvwriter.writerow(updated_record)
    return True


def update_ooo(emp_id, no_of_leaves, start_dt, end_dt):
    """To update out of office(OOO) leaves in csv file"""
    list_data = cf.csv_to_dict(data_file)

    start = (datetime.strptime(start_dt, "%m/%d/%Y")).date()
    end = (datetime.strptime(end_dt, "%m/%d/%Y")).date()

    for record in list_data:
        is_present = False
        if record['empId'] == str(emp_id):
            record['OooLeaves'] = int(record['OooLeaves']) - no_of_leaves
            record['LeaveAppliedFrom'] = start
            record['LeaveAppliedTo'] = end
            record['FlagLeaveApplied'] = True
            is_present = True
            break
    if not is_present:
        logging.exception("EmpId {} not found!".format(emp_id))
        sys.exit()

    list_keys = list(list_data[0].keys())
    csv_file = open(data_file, mode='r+', encoding='UTF8', newline='')
    csv_file.truncate()
    csvwriter = csv.DictWriter(csv_file, list_keys)
    csvwriter.writeheader()
    for updated_record in list_data:
        csvwriter.writerow(updated_record)


def update_maternity(emp_id, start_dt):
    """To update maternity leave flag along with leave start and end date"""
    list_data = cf.csv_to_dict(data_file)

    start = (datetime.strptime(start_dt, "%m/%d/%Y")).date()
    end_dt = start + timedelta(days=28)
    end_dt = end_dt.strftime("%Y-%m-%d")

    for record in list_data:
        is_present = False
        if record['empId'] == str(emp_id):
            record['FlagMaternity'] = True
            record['LeaveAppliedFrom'] = start
            record['LeaveAppliedTo'] = end_dt
            record['Maternity'] = 0
            is_present = True
            break

    if not is_present:
        logging.exception("EmpId {} not found!".format(emp_id))
        sys.exit()

    list_keys = list(list_data[0].keys())
    csv_file = open(data_file, mode='r+', encoding='UTF8', newline='')
    csv_file.truncate()
    csvwriter = csv.DictWriter(csv_file, list_keys)
    csvwriter.writeheader()
    for updated_record in list_data:
        csvwriter.writerow(updated_record)


def update_paternity(emp_id, start_dt):
    """To update paternity leave flag along with leave start and end date"""
    list_data = cf.csv_to_dict(data_file)

    start = (datetime.strptime(start_dt, "%m/%d/%Y")).date()
    end_dt = start + timedelta(days=168)
    end_dt = end_dt.strftime("%Y-%m-%d")

    for record in list_data:
        is_present = False
        if record['empId'] == str(emp_id):
            record['FlagPaternity'] = True
            record['LeaveAppliedFrom'] = start
            record['LeaveAppliedTo'] = end_dt
            record['Paternity'] = 0
            is_present = True
            break

    if not is_present:
        logging.exception("EmpId {} not found!".format(emp_id))
        sys.exit()

    list_keys = list(list_data[0].keys())
    csv_file = open(data_file, mode='r+', encoding='UTF8', newline='')
    csv_file.truncate()
    csvwriter = csv.DictWriter(csv_file, list_keys)
    csvwriter.writeheader()
    for updated_record in list_data:
        csvwriter.writerow(updated_record)


def add_employee(dict_record):
    """Adding new employee's leave details to Db"""

    csv_file = open(data_file, mode='r+', encoding='UTF8', newline='')
    csv_reader = csv.reader(csv_file)
    header = next(csv_reader)
    csvwriter = csv.DictWriter(csv_file, header)

    record = dict_record
    record_leave = {'empId': record['empId'], 'Name': record['Name'], 'JoiningDate': record['JoiningDate'],
                    'Gender': record['Gender']}
    if record_leave['Gender'] == 'F':
        record_leave['Paternity'] = 0
        record_leave['Maternity'] = 28
    else:
        record_leave['Paternity'] = 168
        record_leave['Maternity'] = 0
    record_leave['CompOff'] = ''
    record_leave['FlagMaternity'] = False
    record_leave['FlagPaternity'] = False
    record_leave['FlagLeaveApplied'] = False
    record_leave['LeaveAppliedFrom'] = ''
    record_leave['LeaveAppliedTo'] = ''
    record_leave['NoOfLeavesApplied'] = 0
    record_leave['OooLeaves'] = 0

    csvwriter.writerow(record_leave)
