import UpdateData as ud
import Constants as const
import numpy as np
from datetime import datetime, timedelta
import logging
import RetrieveData as rd
import sys


def apply_leave(emp_id, leave_type, start_dt, end_dt=None):
    if leave_type == 'ooo':
        flag = rd.verify_leave_not_applied(emp_id, start_dt, end_dt)
        if flag:
            logging.exception("You've already applied leaves in the given time period")
            sys.exit()
        no_of_leaves = no_of_weekdays(start_dt, end_dt)
        apply_ooo(emp_id, no_of_leaves, start_dt, end_dt)
    elif leave_type == 'compoff':
        flag = rd.verify_leave_not_applied(emp_id, start_dt, end_dt)
        if flag:
            logging.exception("You've already applied leaves in the given time period")
            sys.exit()
        no_of_leaves = no_of_weekdays(start_dt, end_dt)
        apply_compoff(emp_id, no_of_leaves, start_dt, end_dt)
    elif leave_type == 'maternity':
        apply_maternity(emp_id, start_dt)
    elif leave_type == 'paternity':
        apply_paternity(emp_id, start_dt)
    else:
        logging.exception("Invalid leave type")
        sys.exit()


def apply_compoff(emp_id, count_leaves, start_dt, end_dt):
    compoff_leaves = int(rd.get_compoff(emp_id))
    if compoff_leaves == -1:
        logging.exception("Invalid emp id {}".format(emp_id))
        sys.exit()
    if compoff_leaves == 0:
        logging.exception(
            "You don't have sufficient compoff leaves, maximum compoffs you can apply are {}".format(compoff_leaves))
        sys.exit()
    flag = ud.remove_compoff(emp_id, count_leaves, start_dt, end_dt)
    if not flag:
        logging.exception("You don't have sufficient compoff leaves, maximum compoffs you can apply are {}".format(compoff_leaves))
        sys.exit()


def apply_ooo(emp_id, count_leaves, start_dt, end_dt):
    ooo_leaves = int(rd.get_ooo(emp_id))
    if ooo_leaves == -1:
        logging.exception("Invalid emp id {}".format(emp_id))
        sys.exit()
    if count_leaves == 0:
        logging.exception("Dates for the leave are invalid as they're either a weekend or a public holiday")
    elif count_leaves > ooo_leaves:
        logging.exception("You don't have enough leaves, max leaves you can apply are {}".format(ooo_leaves))
    else:
        ud.update_ooo(emp_id, count_leaves, start_dt, end_dt)


def apply_paternity(emp_id, start_dt):
    paternity_leaves = int(rd.get_paternity(emp_id))
    if paternity_leaves == -1:
        logging.exception("Invalid emp id {}".format(emp_id))
        sys.exit()
    if paternity_leaves == 0:
        logging.exception("You're either not eligible for maternity leave or have already claimed it")
    else:
        ud.update_paternity(emp_id, start_dt)


def apply_maternity(emp_id, start_dt):
    maternity_leaves = int(rd.get_maternity(emp_id))
    if maternity_leaves == -1:
        logging.exception("Invalid emp id {}".format(emp_id))
        sys.exit()
    if maternity_leaves == 0:
        logging.exception("You're either not eligible for maternity leave or have already claimed it")
    else:
        ud.update_maternity(emp_id, start_dt)


def no_of_weekdays(start_dt, end_dt):
    """To get the number of weekdays between two dates"""
    # Converting to date time objects
    start = datetime.strptime(start_dt, "%m/%d/%Y")
    end = datetime.strptime(end_dt, "%m/%d/%Y")

    # generating total days using busday_count()
    count_weekdays = np.busday_count(start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'),
                                     holidays=const.public_holidays)

    return count_weekdays


