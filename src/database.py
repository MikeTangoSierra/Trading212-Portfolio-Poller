import logging
from functions.transform_data_functions import *
from functions.get_data_functions import *
from functions.database_functions import *
from functions.time_functions import *

# Logging config - This needs some work
logging.basicConfig(filename='database.log', encoding='utf-8', level=logging.DEBUG)


# Call date time function to set current date and time
write_date_time = current_date_and_time()

# Set some vars for profit loss
profit_loss_db = "profit_loss"
profit_loss_col = "profit_loss"
profit_loss_value = overall_profit_loss()
profit_loss_dict = {"profit_loss_value": str(profit_loss_value), "updated_time": str(write_date_time)}

# Set some vars for open portfolio positions
open_positions_db = "open_portfolio_positions"
open_positions_col = "open_portfolio_positions"

# For profit loss, check if the document already exists in our collection, if not, write it.
does_document_exist_in_collection = check_if_document_exists_in_mongodb(profit_loss_db, profit_loss_col,
                                                                        profit_loss_dict)

if not does_document_exist_in_collection:
    insert_document_in_mongodb(profit_loss_db, profit_loss_col, profit_loss_dict)

# For open portfolio positions, format our positions into separate dicts, check if the documents already exists in our
# collection, if not, write it.
unformatted_open_positions_values = get_portfolio_positions()

for position in unformatted_open_positions_values:
    open_positions_dict = {"_id": str(position['ticker']), "quantity": str(position['quantity']),
                           "averagePrice": str(position['averagePrice']),
                           "currentPrice": str(position['currentPrice']),
                           "ppl": str(position['ppl']), "fxPpl": str(position['fxPpl']),
                           "initialFillDate": str(position['initialFillDate']),
                           "frontend": str(position['frontend']),
                           "maxBuy": str(position['maxBuy']), "maxSell": str(position['maxSell']),
                           "pieQuantity": str(position['pieQuantity']), "updated_time": str(write_date_time)}

    does_document_exist_in_collection = check_if_document_exists_in_mongodb(open_positions_db, open_positions_col,
                                                                            open_positions_dict)
    if not does_document_exist_in_collection:
        insert_document_in_mongodb(open_positions_db, open_positions_col, open_positions_dict)

# If the documents in our collections are older than a certain time period, then delete them. I need to write this
# functionality next! Consider how long we might need to refer to the documents for in later functionality.


