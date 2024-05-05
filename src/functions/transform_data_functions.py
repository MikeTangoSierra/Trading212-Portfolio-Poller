from functions.get_data_functions import *
import logging

# Logging config - This needs some work.
logging.basicConfig(filename='transform_data_functions.log', encoding='utf-8', level=logging.DEBUG)


# Call functions from get_data_functions to get portfolio equity (overall).
def overall_portfolio_value():
    portfolio_overall_equity = str(get_account_equity_info()['total'])
    portfolio_base_currency = str(get_account_base_currency())
    return portfolio_overall_equity + ":" + " " + portfolio_base_currency


# Call functions from get_data_function to get portfolio profit and loss (overall).
def overall_profit_loss():
    portfolio_profit_loss = str(get_account_equity_info()['ppl'])
    portfolio_base_currency = str(get_account_base_currency())
    return portfolio_profit_loss + ":" + " " + portfolio_base_currency


# Call functions from get_data_function to get currently open positions. Loop over our positions and find our biggest
# losing position.
def currently_open_biggest_loser():
    profit_losses = {}
    portfolio_positions = get_portfolio_positions()
    for position in portfolio_positions:
        ticker = (position['ticker'])
        ppl = (position['ppl'])
        profit_losses.update({ticker: ppl})
    biggest_loser_ticker = min(profit_losses, key=profit_losses.get)
    biggest_loser_value = min(profit_losses.values())
    return biggest_loser_ticker + ":" + " " + str(biggest_loser_value)


# Call functions from get_data_function to get currently open positions. Loop over our positions and find our biggest
# winning position.
def currently_open_biggest_winner():
    profit_losses = {}
    portfolio_positions = get_portfolio_positions()
    for position in portfolio_positions:
        ticker = (position['ticker'])
        ppl = (position['ppl'])
        profit_losses.update({ticker: ppl})
    biggest_loser_ticker = max(profit_losses, key=profit_losses.get)
    biggest_loser_value = max(profit_losses.values())
    return biggest_loser_ticker + ":" + " " + str(biggest_loser_value)
