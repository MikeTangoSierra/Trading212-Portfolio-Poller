import flask
import time
import os
import logging
from functions.time_functions import *
from functions.transform_data_functions import *
from functions.get_data_functions import *
from functions.database_functions import *

# Application Configuration.
app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Logging config - This needs some work.
logging.basicConfig(filename='application_debug.log', encoding='utf-8', level=logging.DEBUG)
logging.basicConfig(filename='application_error.log', encoding='utf-8', level=logging.ERROR)
logging.basicConfig(filename='application_info.log', encoding='utf-8', level=logging.INFO)


# Get overall portfolio equity and expose it on /portfoliovalue endpoint.
@app.route('/portfolio_value', methods=['GET'])
def portfolio_value():
    return overall_portfolio_value()


# Get portfolio profit and loss and expose it on /profitloss endpoint.
@app.route('/profit_loss', methods=['GET'])
def profit_loss():
    if is_market_open():
        return "THE MARKET IS OPEN!" + "\n" + overall_profit_loss()
    else:
        return "THE MARKET IS CLOSED!" + "\n" + overall_profit_loss() + "\n" + "AS OF MARKET CLOSE!"


# Get list of positions in the portfolio and expose them on /portfoliopostions endpoint.
@app.route('/portfolio_postions', methods=['GET'])
def return_portfolio_positions():
    return get_portfolio_positions()


# Work out what our biggest loser is for our currently open positions.
@app.route('/current_biggest_loser', methods=['GET'])
def return_current_biggest_losing_position():
    return currently_open_biggest_loser()


# Work out what our biggest winner is for our currently open positions.
@app.route('/current_biggest_winner', methods=['GET'])
def return_current_biggest_winning_position():
    return currently_open_biggest_winner()

# Work out what our biggest gain is for the current quarter.
@app.route('/biggest_winner_quarterly', methods=['GET'])
def return_biggest_winner_quarterly():
    return get_biggest_winning_position("open_portfolio_positions", "open_portfolio_positions", get_quarter_start_date(), get_current_date_and_time())

# Whilst the market is open, run our database.py script every 60 seconds to update the database with our statistics.
os.system("python /app/src/database.py")
time.sleep(60.0)

# Query database and return the following stats on different endpoints (use functions in database_functions.py for
# this, stick to DRY!) Portfolio gain/loss for the quarter Portfolio gain/loss for the month Portfolio gain/loss for
# the week Portfolio gain/loss for the day Biggest gain/loss (position) for the quarter Biggest gain/loss (position)
# for the month Biggest gain/loss (position) for the week Biggest gain/loss (position) for the day

