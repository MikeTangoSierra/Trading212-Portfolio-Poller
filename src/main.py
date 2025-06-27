from functions.database_functions import *
from functions.get_data_functions import *
from functions.logging import *
from functions.time_functions import *
from functions.transform_data_functions import *
import time
import flask

# Call the logging configuration function.
configure_logging('main_application.log')

# Application Configuration.
app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Variables.
open_portfolio_positions_databases = ["open_portfolio_positions"]
open_portfolio_positions_collections = ["open_portfolio_positions", "open_portfolio_positions_weekly", "open_portfolio_positions_monthly", "open_portfolio_positions_quarterly", "open_portfolio_positions_yearly"]


# Get overall portfolio equity and expose it on the /portfoliovalue endpoint.
@app.route('/portfolio_value', methods=['GET'])
def portfolio_value():
    return overall_portfolio_value()


# Get portfolio profit and loss and expose it on the /profitloss endpoint.
@app.route('/profit_loss', methods=['GET'])
def profit_loss():
    if is_market_open():
        return "THE MARKET IS OPEN!" + "\n" + overall_profit_loss()
    else:
        return "THE MARKET IS CLOSED!" + "\n" + overall_profit_loss() + "\n" + "AS OF MARKET CLOSE!"


# Get list of positions in the portfolio and expose them on the /portfolio_positions endpoint.
@app.route('/portfolio_positions', methods=['GET'])
def return_portfolio_positions():
    return get_portfolio_positions()


# Work out what our biggest gain is for the last day and expose it on the /biggest_winner_daily endpoint.
@app.route('/biggest_winner_daily', methods=['GET'])
def return_biggest_winner_daily():
    return get_biggest_winning_position(open_portfolio_positions_databases, open_portfolio_positions_collections, get_day_start_date(),
                                        get_day_end_date())


# Work out what our biggest gain is for the last week and expose it on the /biggest_winner_weekly endpoint.
@app.route('/biggest_winner_weekly', methods=['GET'])
def return_biggest_winner_weekly():
    return get_biggest_winning_position(open_portfolio_positions_databases, open_portfolio_positions_collections, get_week_start_date(),
                                        get_week_end_date())


# Work out what our biggest gain is for the last month and expose it on the /biggest_winner_monthly endpoint.
@app.route('/biggest_winner_monthly', methods=['GET'])
def return_biggest_winner_monthly():
    return get_biggest_winning_position(open_portfolio_positions_databases, open_portfolio_positions_collections, get_month_start_date(),
                                        get_month_end_date())


# Work out what our biggest gain is for the current quarter and expose it on the /biggest_winner_quarterly endpoint.
@app.route('/biggest_winner_quarterly', methods=['GET'])
def return_biggest_winner_quarterly():
    return get_biggest_winning_position(open_portfolio_positions_databases, open_portfolio_positions_collections,
                                        get_quarter_start_date(), get_quarter_end_date())


# Work out what our biggest loss is for the last day and expose it on the /biggest_loser_daily endpoint.
@app.route('/biggest_loser_daily', methods=['GET'])
def return_biggest_loser_daily():
    return get_biggest_losing_position(open_portfolio_positions_databases, open_portfolio_positions_collections, get_day_start_date(),
                                       get_day_end_date())


# Work out what our biggest loss is for the last week and expose it on the /biggest_loser_weekly endpoint.
@app.route('/biggest_loser_weekly', methods=['GET'])
def return_biggest_loser_weekly():
    return get_biggest_losing_position(open_portfolio_positions_databases, open_portfolio_positions_collections, get_week_start_date(),
                                       get_week_end_date())


# Work out what our biggest loss is for the last month and expose it on the /biggest_loser_monthly endpoint.
@app.route('/biggest_loser_monthly', methods=['GET'])
def return_biggest_loser_monthly():
    return get_biggest_losing_position(open_portfolio_positions_databases, open_portfolio_positions_collections, get_month_start_date(),
                                       get_month_end_date())


# Work out what our biggest loss is for the current quarter and expose it on the /biggest_loser_quarterly endpoint.
@app.route('/biggest_loser_quarterly', methods=['GET'])
def return_biggest_loser_quarterly():
    return get_biggest_losing_position(open_portfolio_positions_databases, open_portfolio_positions_collections, get_quarter_start_date(),
                                       get_quarter_end_date())


# Whilst the market is open, run our database.py script every 60 seconds to update the database with our statistics.
while is_market_open():
    os.system("python /app/src/database.py")
    time.sleep(60.0)

# Query database and return the following stats on different endpoints (use functions in database_functions.py for
# this, stick to DRY!) Portfolio gain/loss for the quarter Portfolio gain/loss for the month Portfolio gain/loss for
# the week Portfolio gain/loss for the day Biggest gain/loss (position) for the quarter Biggest gain/loss (position)
# for the month Biggest gain/loss (position) for the week Biggest gain/loss (position) for the day
