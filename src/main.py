import flask
import pprint
import json
from functions.time_functions import *
from functions.transform_data_functions import *
from functions.get_data_functions import *

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Get portfolio value and expose it on /portfoliovalue endpoint
@app.route('/portfoliovalue', methods=['GET'])
def return_portfolio_value():
    while time_in_range(start, end, current):
        return final_portfolio_value()
    else:
        return("MARKET CLOSED")
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
