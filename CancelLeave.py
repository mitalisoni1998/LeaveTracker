import sys

import UpdateData as ud
import CommonFunctions as cf
import logging
import csv

data_file = "/Users/sonmit01/Documents/Data/EmployeeLeaveData.csv"


def cancel_leave(emp_id):
    list_data = cf.csv_to_dict(data_file)
    for record in list_data:
        if record['empId'] == str(emp_id):
            if record['FlagLeaveApplied'] == 'True':
                record['LeaveAppliedFrom'] = ''
                record['LeaveAppliedTo'] = ''
                record['FlagLeaveApplied'] = False
                no_of_leaves = int(record['NoOfLeavesApplied'])
                record['NoOfLeavesApplied'] = 0
                ooo_leaves = int(record['OooLeaves']) + no_of_leaves
                record['OooLeaves'] = ooo_leaves
                break
            else:
                logging.exception("You have no applied leaves to cancel")
                sys.exit()

    list_keys = list(list_data[0].keys())
    csv_file = open(data_file, mode='r+', encoding='UTF8', newline='')
    csv_file.truncate()
    csvwriter = csv.DictWriter(csv_file, list_keys)
    csvwriter.writeheader()
    for updated_record in list_data:
        csvwriter.writerow(updated_record)