from functions.database_functions import *
from functions.get_data_functions import *
from functions.time_functions import *
from functions.transform_data_functions import *

# Set some variables from the environment.
retain_data_for_days = int(os.environ['RETAIN_DATA_FOR_DAYS'])

# Call the logging configuration function.
configure_logging('database.log')

# Call date time function to set current date and time.
write_date_time = get_current_date_and_time()

# Set some variables for overall portfolio value.
portfolio_value_db = "portfolio_value"
portfolio_value_col = "portfolio_value"
portfolio_value_value = overall_portfolio_value()
portfolio_value_dict = {"portfolio_value": str(portfolio_value_value), "last_updated": str(write_date_time)}

# Insert portfolio value data if it doesn't exist.
if not check_if_document_exists_in_mongodb(portfolio_value_db, portfolio_value_col, portfolio_value_dict):
    insert_document_in_mongodb(portfolio_value_db, portfolio_value_col, portfolio_value_dict)

# Set some variables for profit loss.
profit_loss_db = "profit_loss"
profit_loss_col = "profit_loss"
profit_loss_value = overall_profit_loss()
profit_loss_dict = {"profit_loss_value": str(profit_loss_value), "last_updated": str(write_date_time)}

# Insert profit loss data if it doesn't exist.
if not check_if_document_exists_in_mongodb(profit_loss_db, profit_loss_col, profit_loss_dict):
    insert_document_in_mongodb(profit_loss_db, profit_loss_col, profit_loss_dict)

# Set some variables for open portfolio positions.
open_positions_db = "open_portfolio_positions"
unformatted_open_positions_values = get_portfolio_positions()

# Insert open positions data if it doesn't exist.
# If it's the end of a week, month, quarter or year, we'll insert the data into a new collection.
# We'll then query that collection to get the biggest winner/loser for that time period.

# Loop through the open positions and format them for MongoDB.
for position in unformatted_open_positions_values:
    open_positions_dict = {
        "_id": str(position['ticker']),
        "quantity": str(position['quantity']),
        "averagePrice": str(position['averagePrice']),
        "currentPrice": str(position['currentPrice']),
        "ppl": str(position['ppl']),
        "fxPpl": str(position['fxPpl']),
        "initialFillDate": str(position['initialFillDate']),
        "frontend": str(position['frontend']),
        "maxBuy": str(position['maxBuy']),
        "maxSell": str(position['maxSell']),
        "pieQuantity": str(position['pieQuantity']),
        "last_updated": str(write_date_time)
    }


# This is messy, but there's SO many edge cases to consider here. For example, It could be a weekday, end of a month
# and end of a quarter all at the same time.
if is_a_weekday():
    open_positions_col = "open_portfolio_positions_daily"
    if not check_if_document_exists_in_mongodb(open_positions_db, open_positions_col, open_positions_dict):
        insert_document_in_mongodb(open_positions_db, open_positions_col, open_positions_dict)

if is_end_of_week():
    open_positions_col = "open_portfolio_positions_weekly"
    if not check_if_document_exists_in_mongodb(open_positions_db, open_positions_col, open_positions_dict):
        insert_document_in_mongodb(open_positions_db, open_positions_col, open_positions_dict)

if is_end_of_month():
    open_positions_col = "open_portfolio_positions_monthly"
    if not check_if_document_exists_in_mongodb(open_positions_db, open_positions_col, open_positions_dict):
        insert_document_in_mongodb(open_positions_db, open_positions_col, open_positions_dict)

if is_end_of_quarter():
    open_positions_col = "open_portfolio_positions_quarterly"
    if not check_if_document_exists_in_mongodb(open_positions_db, open_positions_col, open_positions_dict):
        insert_document_in_mongodb(open_positions_db, open_positions_col, open_positions_dict)

if is_end_of_year():
    open_positions_col = "open_portfolio_positions_yearly"
    if not check_if_document_exists_in_mongodb(open_positions_db, open_positions_col, open_positions_dict):
        insert_document_in_mongodb(open_positions_db, open_positions_col, open_positions_dict)

# Run our MongoDB cleanup functionality, cleaning up any documents older than 1000 days.
clean_up_mongodb(time_limit_days=retain_data_for_days)
