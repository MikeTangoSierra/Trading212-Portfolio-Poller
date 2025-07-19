import datetime
from src.functions import logging as configurecustomlogging

# Configure logging
configurecustomlogging.configure_logging('time_functions.log')

# A small function to return true if the time is within the current time is within the range (between start and end).
def is_time_within_range(start, end, current):
    try:
        """Returns whether current is in the range [start, end]"""
        return start <= current <= end
    except:
        logging.error("ERROR:" + " " + "Failed to determine if time is within range of market opening hours.")


# Return true if we're between market opening hours (9AM-10PM for rough market opening hours (UK/US Markets) with
# allowances for daylight savings.
def is_market_open():
    try:
        market_open_time = datetime.time(9, 0, 0)
        market_close_time = datetime.time(22, 0, 0)
        current_time = datetime.datetime.now().time()
        return is_time_within_range(market_open_time, market_close_time, current_time)
    except:
        logging.error("ERROR:" + " " + "Failed to determine if market is open")


# Function to return current date and time in %d/%m/%Y %H:%M:%S" format.
def get_current_date_and_time():
    try:
        current_datetime = datetime.datetime.now()
        dt_string = current_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")
        return dt_string
    except:
        logging.error("ERROR:" + " " + "Failed to get current date and time")


# Function to return the start of the current day in %d/%m/%Y %H:%M:%S" format.
def get_day_start_date():
    current_date = datetime.datetime.now()
    day_start_date = datetime.datetime(current_date.year, current_date.month, current_date.day)
    return day_start_date.strftime("%d/%m/%Y %H:%M:%S")


# Function to return the end of the current day in %d/%m/%Y %H:%M:%S" format.
def get_day_end_date():
    current_date = datetime.datetime.now()
    day_end_date = datetime.datetime(current_date.year, current_date.month, current_date.day, 23, 59, 59)
    return day_end_date.strftime("%d/%m/%Y %H:%M:%S")


# Function to return the start of the current week in %d/%m/%Y %H:%M:%S" format.
def get_week_start_date():
    current_date = datetime.datetime.now()
    current_day = current_date.weekday()
    week_start_date = current_date - datetime.timedelta(days=current_day)
    return week_start_date.strftime("%d/%m/%Y %H:%M:%S")


# Function to return the end of the current week in %d/%m/%Y %H:%M:%S" format.
def get_week_end_date():
    current_date = datetime.datetime.now()
    current_day = current_date.weekday()
    week_end_date = current_date + datetime.timedelta(days=(6 - current_day))
    return week_end_date.strftime("%d/%m/%Y %H:%M:%S")


# Function to return the start of the current quarter in %d/%m/%Y %H:%M:%S" format.
def get_quarter_start_date():
    current_date = datetime.datetime.now()
    current_month = current_date.month
    current_year = current_date.year
    quarter_start_date = None

    if 1 <= current_month <= 3:
        quarter_start_date = datetime.datetime(current_year, 1, 1)
    elif 4 <= current_month <= 6:
        quarter_start_date = datetime.datetime(current_year, 4, 1)
    elif 7 <= current_month <= 9:
        quarter_start_date = datetime.datetime(current_year, 7, 1)
    elif 10 <= current_month <= 12:
        quarter_start_date = datetime.datetime(current_year, 10, 1)

    return quarter_start_date.strftime("%d/%m/%Y %H:%M:%S")


# Function to return the start of the current quarter in %d/%m/%Y %H:%M:%S" format.
def get_quarter_start_date():
    current_date = datetime.datetime.now()
    current_month = current_date.month
    current_year = current_date.year
    quarter_start_date = None

    if 1 <= current_month <= 3:
        quarter_start_date = datetime.datetime(current_year, 1, 1)
    elif 4 <= current_month <= 6:
        quarter_start_date = datetime.datetime(current_year, 4, 1)
    elif 7 <= current_month <= 9:
        quarter_start_date = datetime.datetime(current_year, 7, 1)
    elif 10 <= current_month <= 12:
        quarter_start_date = datetime.datetime(current_year, 10, 1)

    return quarter_start_date.strftime("%d/%m/%Y %H:%M:%S")


# Function to return the end of the current quarter in %d/%m/%Y %H:%M:%S" format.
def get_quarter_end_date():
    current_date = datetime.datetime.now()
    current_month = current_date.month
    current_year = current_date.year
    quarter_end_date = None

    if 1 <= current_month <= 3:
        quarter_end_date = datetime.datetime(current_year, 3, 31)
    elif 4 <= current_month <= 6:
        quarter_end_date = datetime.datetime(current_year, 6, 30)
    elif 7 <= current_month <= 9:
        quarter_end_date = datetime.datetime(current_year, 9, 30)
    elif 10 <= current_month <= 12:
        quarter_end_date = datetime.datetime(current_year, 12, 31)

    return quarter_end_date.strftime("%d/%m/%Y %H:%M:%S")


# Function to return the start of the current month in %d/%m/%Y %H:%M:%S" format.
def get_month_start_date():
    current_date = datetime.datetime.now()
    current_month = current_date.month
    current_year = current_date.year
    month_start_date = datetime.datetime(current_year, current_month, 1)
    return month_start_date.strftime("%d/%m/%Y %H:%M:%S")


# Function to return the end of the current month in %d/%m/%Y %H:%M:%S" format.
def get_month_end_date():
    current_date = datetime.datetime.now()
    current_month = current_date.month
    current_year = current_date.year
    month_end_date = None

    if current_month == 2:
        if current_year % 4 == 0:
            month_end_date = datetime.datetime(current_year, 2, 29)
        else:
            month_end_date = datetime.datetime(current_year, 2, 28)
    elif current_month in [1, 3, 5, 7, 8, 10, 12]:
        month_end_date = datetime.datetime(current_year, current_month, 31)
    else:
        month_end_date = datetime.datetime(current_year, current_month, 30)

    return month_end_date.strftime("%d/%m/%Y %H:%M:%S")


# Function to return the start of the current year in %d/%m/%Y %H:%M:%S" format.
def get_year_start_date():
    current_date = datetime.datetime.now()
    current_year = current_date.year
    year_start_date = datetime.datetime(current_year, 1, 1)
    return year_start_date.strftime("%d/%m/%Y %H:%M:%S")


# Function to return the end of the current year in %d/%m/%Y %H:%M:%S" format.
def get_year_end_date():
    current_date = datetime.datetime.now()
    current_year = current_date.year
    year_end_date = datetime.datetime(current_year, 12, 31)
    return year_end_date.strftime("%d/%m/%Y %H:%M:%S")

# Function to figure out if it's Monday to Friday (the market is closed on the weekends).
def is_a_weekday():
    today = datetime.datetime.today().weekday()
    return today in range(0, 5)  # Monday to Friday

# Function to figure out if it's the end of the week.
def is_end_of_week():
    today = datetime.datetime.today().weekday()
    return today == 6  # Sunday


# Function to figure out if it's the end of the month.
def is_end_of_month():
    today = datetime.datetime.today()
    next_day = today + datetime.timedelta(days=1)
    return today.month != next_day.month


# Function to figure out if it's the end of the quarter.
def is_end_of_quarter():
    today = datetime.datetime.today()
    current_quarter = (today.month - 1) // 3 + 1
    next_day = today + datetime.timedelta(days=1)
    next_quarter = (next_day.month - 1) // 3 + 1
    return current_quarter != next_quarter


# Function to figure out if it's the end of the year.
def is_end_of_year():
    today = datetime.datetime.today()
    next_day = today + datetime.timedelta(days=1)
    return today.year != next_day.year
