import datetime
import logging

# Logging config - This needs some work.
logging.basicConfig(filename='time_functions.log', encoding='utf-8', level=logging.DEBUG)


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
        is_time_within_range(market_open_time, market_close_time, current_time)
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

# Function to return the end of the current quarter.
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