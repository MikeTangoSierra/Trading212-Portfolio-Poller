from functions.get_data_functions import *
from functions.time_functions import *

# Call functions from get_data_functions to get portfolio value and currency, add their outputs and print them
def final_portfolio_value():
    portfolio_amount_string = str(get_account_equity())
    portfolio_currency_string = str(get_account_base_currency())
    return(portfolio_amount_string + " " + portfolio_currency_string)
