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
        current = datetime.datetime.now().time()
        is_time_within_range(market_open_time, market_close_time, current)
    except:
        logging.error("ERROR:" + " " + "Failed to determine if market is open")


# Function to return current date and time in %d/%m/%Y %H:%M:%S" format.
def current_date_and_time():
    try:
        current_datetime = datetime.datetime.now()
        dt_string = current_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")
        return dt_string
    except:
        logging.error("ERROR:" + " " + "Failed to get current date and time")
