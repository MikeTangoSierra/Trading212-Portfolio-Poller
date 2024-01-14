import flask
import time
import os
from functions.time_functions import *
from functions.transform_data_functions import *
from functions.get_data_functions import *

# Application Configuration
app = flask.Flask(__name__)
app.config["DEBUG"] = True
database_write_start_time = time.monotonic()


# Get overall portfolio equity and exposse it on /portfoliovalue endpoint
@app.route('/portfoliovalue', methods=['GET'])
def portfolio_value():
    return overall_portfolio_value()


# Get portfolio profit and loss and expose it on /profitloss endpoint
@app.route('/profitloss', methods=['GET'])
def profit_loss():
    while time_in_range(start, end, current):
        return overall_profit_loss()
    else:
        return "MARKET CLOSED"
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


# Call our database.py script every 60 seconds from the database_write_start_time (I should probably update this to
# be only every 5 minutes) I NEED TO ADD FUNCTIONALITY SO THIS DOESN'T RUN WHEN THE MARKETS ARE CLOSED (9AM - 9PM
# GMT/BST)
while True:
    os.system("python /app/src/database.py")
    time.sleep(60.0 - ((time.monotonic() - database_write_start_time) % 60.0))
