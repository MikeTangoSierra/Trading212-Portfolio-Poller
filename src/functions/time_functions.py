import datetime
import time

# Set start (market open, UK), end (markets closed, UK & US) and current times. Setting here as they should never change!
start = datetime.time(9, 0, 0)
end = datetime.time(21, 00, 0)
current = datetime.datetime.now().time()

# Function to figure out if the time is within the range
def time_in_range(start, end, current):
    return start <= current <= end

def sleep_function(seconds):
    time.sleep(30)
