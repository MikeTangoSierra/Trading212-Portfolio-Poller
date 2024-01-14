from datetime import datetime


# Function to return current date and time in %d/%m/%Y %H:%M:%S" format
def current_date_and_time():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    return dt_string
