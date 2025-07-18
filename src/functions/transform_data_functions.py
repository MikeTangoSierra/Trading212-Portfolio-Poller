import logging
import time
from src.functions import logging as configurecustomlogging
from src.functions.get_data_functions import *

# Configure logging
configurecustomlogging.configure_logging('transform_data_functions.log')

# Set some variables that we'll use in our functions.
portfolio_base_currency = str(get_account_base_currency())
while portfolio_base_currency == "None" or portfolio_base_currency == "NONE":
    time.sleep(10)
    portfolio_base_currency = str(get_account_base_currency())

# Call functions from get_data_functions to get portfolio equity (overall).
def overall_portfolio_value():
    try:
        portfolio_overall_equity = str(get_account_equity_info()['total'])
        print(portfolio_overall_equity)
        while portfolio_overall_equity == "None" or portfolio_overall_equity == "NONE":
            time.sleep(10)
            portfolio_overall_equity = str(get_account_equity_info()['total'])
        return portfolio_overall_equity + ":" + " " + portfolio_base_currency
    except:
        logging.error("ERROR:" + " " + "Failed to get overall portfolio value")


# Call functions from get_data_function to get portfolio profit and loss (overall).
def overall_profit_loss():
    try:
        portfolio_profit_loss = str(get_account_equity_info()['ppl'])
        print(portfolio_profit_loss)
        while portfolio_profit_loss == "None" or portfolio_profit_loss == "NONE":
            time.sleep(10)
            portfolio_profit_loss = str(get_account_equity_info()['ppl'])
        return portfolio_profit_loss + ":" + " " + portfolio_base_currency
    except:
        logging.error("ERROR:" + " " + "Failed to get overall profit and loss")


# Call functions from get_data_function to get currently open positions. Loop over our positions and find our biggest
# losing position.
def currently_open_biggest_loser():
    try:
        profit_losses = {}
        portfolio_positions = get_portfolio_positions()

        while portfolio_positions == []:
            time.sleep(10)
            portfolio_positions = get_portfolio_positions()

        for position in portfolio_positions:
            ticker = (position['ticker'])
            ppl = (position['ppl'])
            profit_losses.update({ticker: ppl})

        biggest_loser_ticker = min(profit_losses, key=profit_losses.get)
        biggest_loser_value = min(profit_losses.values())

        return biggest_loser_ticker + ":" + " " + str(biggest_loser_value)
    except:
        logging.error("ERROR:" + " " + "Failed to get current biggest loser")


# Call functions from get_data_function to get currently open positions. Loop over our positions and find our biggest
# winning position.
def currently_open_biggest_winner():
    try:
        profit_losses = {}
        portfolio_positions = get_portfolio_positions()
        while portfolio_positions == [{}]:
            time.sleep(10)
            portfolio_positions = get_portfolio_positions()

        for position in portfolio_positions:
            ticker = (position['ticker'])
            ppl = (position['ppl'])
            profit_losses.update({ticker: ppl})

        biggest_loser_ticker = max(profit_losses, key=profit_losses.get)
        biggest_loser_value = max(profit_losses.values())
        return biggest_loser_ticker + ":" + " " + str(biggest_loser_value)
    except:
        logging.error("ERROR:" + " " + "Failed to get current biggest winner")
