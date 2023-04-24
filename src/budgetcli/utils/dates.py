import calendar
from datetime import datetime


def get_current_month():
    """An utility function to return the current month number"""
    now = datetime.now()
    return now.month


def get_month_number(month: str) -> int | None:
    """An utility function to return the month number from the month name"""
    month_str = month.lower()
    for i, month in enumerate(calendar.month_name[1:], 1):
        abbr = calendar.month_abbr[i].lower()
        if month_str == month.lower() or month_str == abbr:
            return i
