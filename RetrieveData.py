import csv
import logging
import sys
import ast
from datetime import datetime
from datetime import timedelta

import CommonFunctions as cf

data_file = "/Users/sonmit01/Documents/Data/EmployeeLeaveData.csv"


def get_ooo(emp_id):
    list_data = cf.csv_to_dict(data_file)
    for record in list_data:
        if record['empId'] == str(emp_id):
            ooo_leaves = record['OooLeaves']
            return ooo_leaves
    return -1


def get_maternity(emp_id):
    list_data = cf.csv_to_dict(data_file)
    for record in list_data:
        if record['empId'] == str(emp_id):
            maternity_leaves = record['Maternity']
            return maternity_leaves
    return -1


def get_paternity(emp_id):
    list_data = cf.csv_to_dict(data_file)
    for record in list_data:
        if record['empId'] == str(emp_id):
            paternity_leaves = record['Paternity']
            return paternity_leaves
    return -1


def get_compoff(emp_id):
    list_data = cf.csv_to_dict(data_file)
    for record in list_data:
        if record['empId'] == str(emp_id):
            if record['CompOff'] == '':
                return 0
            else:
                dict_compoff = ast.literal_eval(record['CompOff'])  # Convert dictionary string to a dictionary object
                dict_compoff_keys = list(dict_compoff.keys())
                compoff_available = 0
                for key in dict_compoff_keys:
                    compoff_available += int(dict_compoff[key])
                return compoff_available
                break
    return -1


def verify_leave_not_applied(emp_id, start_dt, end_dt):
    list_data = cf.csv_to_dict(data_file)
    for record in list_data:
        if record['empId'] == str(emp_id):
            flag_m = eval(record['FlagMaternity'])
            flag_p = eval(record['FlagPaternity'])
            flag_l = eval(record['FlagLeaveApplied'])
            value = flag_m or flag_p or flag_l
            if value:
                start = record['LeaveAppliedFrom']
                end = record['LeaveAppliedTo']
                start = datetime.strptime(start, '%Y-%m-%d')
                end = datetime.strptime(end, '%Y-%m-%d')
                leave_start = datetime.strptime(start_dt, '%m/%d/%Y')
                leave_end = datetime.strptime(end_dt, '%m/%d/%Y')
                while leave_start < leave_end:
                    if start <= leave_start <= end:
                        return True
                    else:
                        leave_start = leave_start + timedelta(days=1)
                return False
