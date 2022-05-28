import csv
from datetime import datetime
import schedule
import EmployeeData as ed
from datetime import date
from datetime import datetime


def create_db():
    """Creating a csv file to act as a database for the employee leave data"""

    header = ['empId', 'Name', 'JoiningDate', 'Gender', 'OooLeaves', 'CompOff', 'Paternity', 'Maternity',
              'FlagMaternity', 'FlagPaternity',
              'FlagLeaveApplied', 'LeaveAppliedFrom', 'LeaveAppliedTo', 'NoOfLeavesApplied']

    list_empdata = ed.load_employee_data()
    csv_file = open("/Users/sonmit01/Documents/Data/EmployeeLeaveData.csv", mode='w')
    csv_file = open("/Users/sonmit01/Documents/Data/EmployeeLeaveData.csv", mode='r+', encoding='UTF8', newline='')
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
            record_leave['CompOff'] = []
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
