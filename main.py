# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import EmployeeData as ed
import UpdateData as ud
import ast
import ApplyLeaves as al

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # ed.add_employee("Mitali Soni")
    # ed.load_employee_data()
    # ud.create_db()
    # ud.get_no_of_months('03/02/2021')
    # ud.update_ooo(100,-1)
    # ud.update_maternity(101, '05/28/2022')
    # ud.add_compoff(102,1)
    # ud.remove_compoff(100, 2, '05/28/2022', '05/30/2022')
    # print()
    # ed.add_employee("Dhruv Soni", "M")
     al.apply_leave(102, 'ooo', '06/01/2022', '06/02/2022')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
