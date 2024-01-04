from functions.get_data_functions import *
from functions.time_functions import *

# Call functions from get_data_functions to get portfolio value and currency, add their outputs and print them
def final_portfolio_value():
    portfolio_amount_string = str(get_account_equity())
    portfolio_currency_string = str(get_account_base_currency())
    return(portfolio_amount_string + " " + portfolio_currency_string)

# Call functions from get_data_functions to get currently open positions. Loop over our postions and find our biggest losing position
def currently_open_biggest_loser():
  profit_losses = {}
  portfolio_positions = get_portfolio_positions()
  for position in portfolio_positions:
      ticker = (position['ticker'])
      ppl = (position['ppl'])
      profit_losses.update({ticker:ppl})
  biggest_loser_ticker = min(profit_losses, key=profit_losses.get)
  biggest_loser_value  = min(profit_losses.values())
  return(biggest_loser_ticker + ":" + " " + str(biggest_loser_value))

# Call functions from get_data_functions to get currently open positions. Loop over our postions and find our biggest winning position
def currently_open_biggest_winner():
    profit_losses = {}
    portfolio_positions = get_portfolio_positions()
    for position in portfolio_positions:
        ticker = (position['ticker'])
        ppl = (position['ppl'])
        profit_losses.update({ticker:ppl})
    biggest_loser_ticker = max(profit_losses, key=profit_losses.get)
    biggest_loser_value  = max(profit_losses.values())
    return(biggest_loser_ticker + ":" + " " + str(biggest_loser_value))