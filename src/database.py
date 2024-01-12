from functions.transform_data_functions import *
from functions.get_data_functions import *
from functions.database_functions import *


# Set some DB related vars
profit_loss_db = "profit_loss"
profit_loss_col = "profit_loss"
open_positions_db = "open_portfolio_positions"
open_positions_col = "open_portfolio_positions"

# Write profit loss to our database, updating on a one minute interval
profit_loss_value = overall_profit_loss()
profit_loss_dict = {"profit_loss_value": str(profit_loss_value)}
insert_document_in_mongodb(profit_loss_db, profit_loss_col, profit_loss_dict)

# Loop through our open positions, create a dict for each of them, write our open positions to our database,
# inserting/updating on a one minute interval
unformatted_open_positions_values = get_portfolio_positions()

for position in unformatted_open_positions_values:
    open_positions_dict = {"_id": str(position['ticker']), "quantity": str(position['quantity']),
                           "averagePrice": str(position['averagePrice']), "currentPrice": str(position['currentPrice']),
                           "ppl": str(position['ppl']), "fxPpl": str(position['fxPpl']),
                           "initialFillDate": str(position['initialFillDate']), "frontend": str(position['frontend']),
                           "maxBuy": str(position['maxBuy']), "maxSell": str(position['maxSell']),
                           "pieQuantity": str(position['pieQuantity'])}

    insert_document_in_mongodb(open_positions_db, open_positions_col, open_positions_dict)