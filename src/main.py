import flask
import time
import os
import logging
from functions.time_functions import *
from functions.transform_data_functions import *
from functions.get_data_functions import *

# Application Configuration.
app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Logging config - This needs some work.
logging.basicConfig(filename='application_debug.log', encoding='utf-8', level=logging.DEBUG)
logging.basicConfig(filename='application_error.log', encoding='utf-8', level=logging.ERROR)
logging.basicConfig(filename='application_info.log', encoding='utf-8', level=logging.INFO)


# Get overall portfolio equity and exposse it on /portfoliovalue endpoint.
@app.route('/portfoliovalue', methods=['GET'])
def portfolio_value():
    return overall_portfolio_value()


# Get portfolio profit and loss and expose it on /profitloss endpoint.
@app.route('/profitloss', methods=['GET'])
def profit_loss():
    if is_market_open():
        return overall_profit_loss()
    else:
        return "MARKET CLOSED"
        # Need to update this to return "MARKET CLOSED + PORTFOLIO CLOSING VALUE"


# Get list of positions in the portfolio and expose them on /portfoliopostions endpoint.
@app.route('/portfoliopostions', methods=['GET'])
def return_portfolio_positions():
    return get_portfolio_positions()


# Work out what our biggest loser is for our currently open positions.
@app.route('/currentbiggestloser', methods=['GET'])
def return_current_biggest_losing_position():
    return currently_open_biggest_loser()


# Work out what our biggest winner is for our currently open positions.
@app.route('/currentbiggestwinner', methods=['GET'])
def return_current_biggest_winning_position():
    return currently_open_biggest_winner()


# Whilst the market is open, run our database.py script every 60 seconds to update the database with our statistics.
if is_market_open():
    while True:
        os.system("python /app/src/database.py")
        time.sleep(60.0)

# Query database and return the following stats on different endpoints (use functions in database_functions.py for
# this, stick to DRY!) Portfolio gain/loss for the quarter Portfolio gain/loss for the month Portfolio gain/loss for
# the week Portfolio gain/loss for the day Biggest gain/loss (position) for the quarter Biggest gain/loss (position)
# for the month Biggest gain/loss (position) for the week Biggest gain/loss (position) for the day

