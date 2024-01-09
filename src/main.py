import flask
from functions.time_functions import *
from functions.transform_data_functions import *
from functions.get_data_functions import *
from functions.write_to_database import *

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Get overall portfolio equity and exposse it on /portfoliovalue endpoint
@app.route('/portfoliovalue', methods=['GET'])
def portfolio_value():
    while time_in_range(start, end, current):
        return overall_portfolio_value()
    else:
        return ("MARKET CLOSED")
        # Need to update this to return "MARKET CLOSED + PORTFOLIO CLOSING VALUE"


# Get portfolio profit and loss and expose it on /profitloss endpoint
@app.route('/profitloss', methods=['GET'])
def profit_loss():
    while time_in_range(start, end, current):
        return overall_profit_loss()
    else:
        return ("MARKET CLOSED")
        # Need to update this to return "MARKET CLOSED + PORTFOLIO CLOSING VALUE"


# Get list of positions in the portfolio and expose them on /portfoliopostions endpoint
@app.route('/portfoliopostions', methods=['GET'])
def return_portfolio_positions():
    return get_portfolio_positions()


# Work out what our biggest loser is for our currently open positions
@app.route('/currentbiggestloser', methods=['GET'])
def return_current_biggest_losing_position():
    return currently_open_biggest_loser()


# Work out what our biggest winner is for our currently open positions
@app.route('/currentbiggestwinner', methods=['GET'])
def return_current_biggest_winning_position():
    return currently_open_biggest_winner()


# I'LL MOVE THIS TO A SEPARATE FILE AND CALL THAT FILE HERE WHEN I'VE FINISHED IT/IT WORKS AND BEFORE MERGE
# Set some DB related vars
overall_profit_loss_db = "profit_loss"
overall_profit_loss_col = "profit_loss"
open_positions_db = "open_portfolio_positions"
open_positions_col = "open_portfolio_positions"

# Intiate our databases and their initial collections. We do this as you must try to write something to a mongoDB for it to actually be created.
create_initial_mongodb(overall_profit_loss_db, overall_profit_loss_col)
create_initial_mongodb(open_positions_db, open_positions_col)

# Write profit loss to our database, updating on a one minute interval
profit_loss_value = overall_profit_loss()
profit_loss_dict = {"profit_loss_value": str(profit_loss_value)}
insert_document_in_mongodb(overall_profit_loss_db,overall_profit_loss_col,profit_loss_dict)

# Loop through our open positions, create a dict for each of them, write our open positions to our database, inserting/updating on a one minute interval
unformatted_open_positions_values = get_portfolio_positions()

for position in unformatted_open_positions_values:
    open_positions_dict = {"_id": str(position['ticker']), "quantity": str(position['quantity']), "averagePrice": str(position['averagePrice']), "currentPrice": str(position['currentPrice']), "ppl": str(position['ppl']), "fxPpl": str(position['fxPpl']), "initialFillDate": str(position['initialFillDate']), "frontend": str(position['frontend']), "maxBuy": str(position['maxBuy']), "maxSell": str(position['maxSell']), "pieQuantity": str(position['pieQuantity'])}

    insert_document_in_mongodb(open_positions_db,open_positions_col,open_positions_dict)

