import flask
from functions.time_functions import *
from functions.transform_data_functions import *
from functions.get_data_functions import *

app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/portfoliovalue', methods=['GET'])
def return_portfolio_value():
    while time_in_range(start, end, current):
        return final_portfolio_value()
    else:
        return("MARKET CLOSED")

@app.route('/portfoliopostions', methods=['GET'])
def return_portfolio_positions():
    return get_portfolio_positions()

app.run()